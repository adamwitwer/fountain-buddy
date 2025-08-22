## Goal of This Project

The goal of this project is to create a system that can automatically identify birds in images, and *most importantly* for the classifications to get more accurate over time, based on human corrections. As long as the human is continuing to make corrections and verifications, the system should continue to improve.

## Description of the Human-in-the-Loop Workflow

1. Our Reolink camera indicates that motion has been detected.
2. YOLO bird detection determines whether the motion is a bird.
3. If it is a brid, the image is passed to the custom CNN model for classification.
4. The custom CNN model returns a classification, along with a confidence score.
5. The system posts the classification to Discord, along with the image and a list of options for the user to select from.
6. The user selects the correct classification from the list.
7. The system updates the database with the correct classification, and renames the image file to include the correct classification.
8. Alternatively, the user can reply with "skip" because of poor image quality, which signals to the system that the image should not be used for training.
9. Sometimes, the user fails to respond to a Discord message, but that does not indicate that the classification is correct. Classification not verified or corrections not made should be used to improve the model.

## Notes About Working in this Project

Please activate the virtual environment by running the following command:

source venv/bin/activate

It's not necessary to create a new virtual environment; use the one that was created by the setup script.

