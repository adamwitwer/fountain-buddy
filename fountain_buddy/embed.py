"""Frozen foundation-model features for bird crops.

Each crop is padded to a square (never center-cropped, which can cut off a head or tail),
then preprocessed the way its model expects. Features are L2-normalized. Embeddings are
cached per model in data/embeddings/<model>.npz, keyed by crop path.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cache
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageOps

MODELS = {
    "bioclip2": ("open_clip", "hf-hub:imageomics/bioclip-2"),
    "dinov3-l": ("timm", "vit_large_patch16_dinov3.lvd1689m"),
    "dinov3-b": ("timm", "vit_base_patch16_dinov3.lvd1689m"),
}
PAD_COLOR = (124, 116, 104)  # ImageNet mean, as RGB


def device() -> str:
    return "mps" if torch.backends.mps.is_available() else "cpu"


@cache
def load(name: str):
    """Return (model, preprocess) for a registered model, on the best device."""
    kind, ref = MODELS[name]
    if kind == "open_clip":
        import open_clip

        model, _, preprocess = open_clip.create_model_and_transforms(ref)
    else:
        import timm

        model = timm.create_model(ref, pretrained=True, num_classes=0)
        cfg = timm.data.resolve_data_config({}, model=model)
        preprocess = timm.data.create_transform(**cfg)
    return model.to(device()).eval(), preprocess


def pad_square(img: Image.Image) -> Image.Image:
    side = max(img.size)
    return ImageOps.pad(img.convert("RGB"), (side, side), color=PAD_COLOR)


@torch.inference_mode()
def embed_images(name: str, images: Sequence[Image.Image], batch: int = 32) -> np.ndarray:
    model, preprocess = load(name)
    out = []
    for i in range(0, len(images), batch):
        x = torch.stack([preprocess(pad_square(im)) for im in images[i : i + batch]])
        x = x.to(device())
        feats = model.encode_image(x) if hasattr(model, "encode_image") else model(x)
        feats = torch.nn.functional.normalize(feats.float(), dim=-1)
        out.append(feats.cpu().numpy())
    return np.concatenate(out) if out else np.zeros((0, 0), np.float32)


def embed_paths(name: str, paths: Sequence[Path], cache_file: Path) -> np.ndarray:
    """Embed image files, reusing anything already in cache_file."""
    keys = [str(p) for p in paths]
    cached: dict[str, np.ndarray] = {}
    if cache_file.exists():
        with np.load(cache_file, allow_pickle=False) as z:
            cached = dict(zip(z["keys"].tolist(), z["feats"], strict=True))
    todo = [k for k in dict.fromkeys(keys) if k not in cached]
    for i in range(0, len(todo), 256):
        chunk = todo[i : i + 256]
        feats = embed_images(name, [Image.open(k) for k in chunk])
        cached.update(zip(chunk, feats, strict=True))
        print(f"  {name}: embedded {min(i + 256, len(todo))}/{len(todo)}", flush=True)
    if todo:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        all_keys = list(cached)
        np.savez(cache_file, keys=np.array(all_keys), feats=np.stack([cached[k] for k in all_keys]))
    return np.stack([cached[k] for k in keys])


@torch.inference_mode()
def embed_texts(name: str, texts: Sequence[str]) -> np.ndarray:
    """Text features for zero-shot classification (open_clip models only)."""
    import open_clip

    model, _ = load(name)
    tokenizer = open_clip.get_tokenizer(MODELS[name][1])
    feats = model.encode_text(tokenizer(list(texts)).to(device()))
    return torch.nn.functional.normalize(feats.float(), dim=-1).cpu().numpy()
