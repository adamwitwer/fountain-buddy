#!/usr/bin/env python3
"""
Model Evaluation Dashboard
Analyzes model performance over time to track improvements
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from collections import defaultdict

class ModelEvaluationDashboard:
    def __init__(self, models_dir='models', db_path='fountain_buddy.db'):
        self.models_dir = Path(models_dir)
        self.db_path = db_path
    
    def load_training_history(self):
        """Load all training metadata files to analyze improvement over time"""
        print("📊 Loading training history...")
        
        history = []
        
        # Find all metadata files
        metadata_files = list(self.models_dir.glob("*_metadata.json"))
        
        for metadata_file in sorted(metadata_files):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Extract key metrics
                training_date = datetime.fromisoformat(metadata['training_date'].replace('Z', '+00:00').replace('+00:00', ''))
                
                record = {
                    'training_date': training_date,
                    'file': metadata_file.name,
                    'best_val_accuracy': metadata.get('best_val_accuracy', 0),
                    'final_val_accuracy': metadata.get('final_val_accuracy', 0),
                    'epochs_completed': metadata.get('epochs_completed', 0),
                    'num_classes': metadata.get('num_classes', 0),
                    'total_training_samples': metadata.get('total_training_samples', 0),
                    'total_validation_samples': metadata.get('total_validation_samples', 0),
                }
                
                # Extract evaluation metrics if available
                if 'evaluation_metrics' in metadata:
                    eval_metrics = metadata['evaluation_metrics']
                    record.update({
                        'per_species_accuracy': eval_metrics.get('per_species_accuracy', {}),
                        'confidence_analysis': eval_metrics.get('confidence_analysis', {}),
                        'human_sample_ratio': eval_metrics.get('dataset_quality_metrics', {}).get('human_sample_ratio', 0),
                        'total_human_samples': eval_metrics.get('dataset_quality_metrics', {}).get('total_human_samples', 0)
                    })
                
                history.append(record)
                
            except Exception as e:
                print(f"⚠️ Error loading {metadata_file}: {e}")
        
        print(f"✅ Loaded {len(history)} training records")
        return sorted(history, key=lambda x: x['training_date'])
    
    def analyze_improvement_trends(self, history):
        """Analyze improvement trends over time"""
        if len(history) < 2:
            print("📈 Need at least 2 training records to analyze trends")
            return
        
        print("\n🔍 IMPROVEMENT TREND ANALYSIS")
        print("=" * 50)
        
        # Overall accuracy trend
        print("📊 Overall Validation Accuracy Trend:")
        for i, record in enumerate(history):
            date_str = record['training_date'].strftime('%Y-%m-%d %H:%M')
            accuracy = record['best_val_accuracy']
            
            if i > 0:
                prev_accuracy = history[i-1]['best_val_accuracy']
                change = accuracy - prev_accuracy
                change_icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                change_str = f" ({change:+.3f})"
            else:
                change_icon = "🎯"
                change_str = " (baseline)"
            
            print(f"  {change_icon} {date_str}: {accuracy:.3f}{change_str}")
        
        # Dataset quality trend
        if any('human_sample_ratio' in record for record in history):
            print("\n🏆 Dataset Quality Trend (Human Sample Ratio):")
            for i, record in enumerate(history):
                if 'human_sample_ratio' not in record:
                    continue
                    
                date_str = record['training_date'].strftime('%Y-%m-%d %H:%M')
                ratio = record['human_sample_ratio']
                human_count = record.get('total_human_samples', 0)
                
                if i > 0 and 'human_sample_ratio' in history[i-1]:
                    prev_ratio = history[i-1]['human_sample_ratio']
                    change = ratio - prev_ratio
                    change_icon = "🚀" if change > 0 else "⬇️" if change < 0 else "➡️"
                    change_str = f" ({change:+.1%})"
                else:
                    change_icon = "📍"
                    change_str = " (baseline)"
                
                print(f"  {change_icon} {date_str}: {ratio:.1%} ({human_count} human samples){change_str}")
    
    def analyze_species_performance(self, history):
        """Analyze per-species performance trends"""
        print("\n🐦 SPECIES-SPECIFIC PERFORMANCE ANALYSIS")
        print("=" * 50)
        
        # Collect species data from latest training
        latest_record = history[-1] if history else None
        if not latest_record or 'per_species_accuracy' not in latest_record:
            print("❌ No per-species accuracy data available")
            return
        
        species_accuracy = latest_record['per_species_accuracy']
        
        # Sort species by accuracy (best to worst)
        sorted_species = sorted(species_accuracy.items(), 
                              key=lambda x: x[1]['accuracy'], reverse=True)
        
        print("🏆 Species Performance Ranking (Latest Model):")
        for i, (species, stats) in enumerate(sorted_species[:10]):  # Top 10
            accuracy = stats['accuracy']
            total = stats['total']
            rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1:2d}."
            
            # Performance indicator
            if accuracy >= 0.9:
                perf_icon = "🔥"  # Excellent
            elif accuracy >= 0.8:
                perf_icon = "✅"  # Good
            elif accuracy >= 0.7:
                perf_icon = "⚠️"   # Needs improvement
            else:
                perf_icon = "❌"  # Poor
            
            print(f"  {rank_icon} {species.replace('_', ' '):25}: {accuracy:.3f} {perf_icon} ({total} validation samples)")
        
        # Show worst performers
        if len(sorted_species) > 10:
            print(f"\n📉 Species Needing Most Improvement:")
            for species, stats in sorted_species[-5:]:  # Bottom 5
                accuracy = stats['accuracy']
                total = stats['total']
                print(f"  ❌ {species.replace('_', ' '):25}: {accuracy:.3f} ({total} validation samples)")
    
    def analyze_confidence_calibration(self, history):
        """Analyze confidence calibration over time"""
        print("\n🎯 CONFIDENCE CALIBRATION ANALYSIS")
        print("=" * 50)
        
        latest_record = history[-1] if history else None
        if not latest_record or 'confidence_analysis' not in latest_record:
            print("❌ No confidence analysis data available")
            return
        
        confidence_stats = latest_record['confidence_analysis']
        calibration = confidence_stats.get('calibration_by_bin', {})
        
        print("📊 Confidence vs Actual Accuracy (Latest Model):")
        for bin_name, stats in calibration.items():
            accuracy = stats['accuracy']
            count = stats['count']
            expected_min = stats['expected_min']
            
            # Check calibration quality
            if bin_name == 'very_high':
                calibration_quality = "🎯" if accuracy >= 0.85 else "⚠️" if accuracy >= 0.75 else "❌"
            elif bin_name == 'high':
                calibration_quality = "🎯" if accuracy >= 0.7 else "⚠️" if accuracy >= 0.6 else "❌"
            else:
                calibration_quality = "✅" if accuracy >= expected_min else "⚠️"
            
            print(f"  {calibration_quality} {bin_name.replace('_', ' ').title():12} ({expected_min:.0%}+): {accuracy:.3f} actual accuracy ({count} samples)")
        
        # Overall confidence stats
        print(f"\n📈 Overall Confidence Statistics:")
        print(f"  Mean confidence: {confidence_stats.get('mean_confidence', 0):.3f}")
        print(f"  Median confidence: {confidence_stats.get('median_confidence', 0):.3f}")
        print(f"  Std deviation: {confidence_stats.get('std_confidence', 0):.3f}")
    
    def analyze_real_world_performance(self):
        # Analyze real-world correction patterns from database
        print("\n🌍 REAL-WORLD PERFORMANCE ANALYSIS (Last 30 Days)")
        print("=" * 50)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_date = datetime.now() - timedelta(days=30)
            
            # This query now compares the AI's guess (ai_species) with the final human-verified species.
            # It only includes records that have been human-verified (confidence = 1.0)
            # and filters out non-bird/skipped classifications.
            query = """
                SELECT
                    ai_species,
                    species AS human_species
                FROM bird_visits
                WHERE timestamp >= ?
                  AND confidence = 1.0
                  AND ai_species IS NOT NULL
                  AND species NOT IN ('Skip', 'Unknown Bird', 'Unknown; Not A Bird', 'Not A Bird', 'Poor Quality - Skipped')
            """
            
            cursor.execute(query, (start_date.strftime('%Y-%m-%d %H:%M:%S'),))
            results = cursor.fetchall()
            conn.close()

            if not results:
                print("❌ No human-verified records found in the last 30 days to analyze.")
                return

            # Process the results into a more usable format
            performance_data = defaultdict(lambda: {'correct': 0, 'incorrect': 0, 'total': 0})
            total_correct = 0
            total_incorrect = 0

            for ai_guess, human_label in results:
                # Standardize for comparison
                ai_guess_clean = ai_guess.strip().title()
                human_label_clean = human_label.strip().title()

                performance_data[human_label_clean]['total'] += 1
                if ai_guess_clean == human_label_clean:
                    performance_data[human_label_clean]['correct'] += 1
                    total_correct += 1
                else:
                    performance_data[human_label_clean]['incorrect'] += 1
                    total_incorrect += 1
            
            total_predictions = total_correct + total_incorrect

            print(f"📊 Species-Specific AI Accuracy (Human-Verified):")
            print("Species                    | Correct | Incorrect | AI Accuracy")
            print("-" * 80)

            # Sort by the number of total observations for that species
            sorted_species = sorted(performance_data.items(), key=lambda item: item[1]['total'], reverse=True)

            for species, data in sorted_species[:15]: # Top 15 species
                accuracy = data['correct'] / data['total'] if data['total'] > 0 else 0
                perf_icon = "🔥" if accuracy >= 0.9 else "✅" if accuracy >= 0.75 else "⚠️" if accuracy >= 0.5 else "❌"
                print(f"{species[:25]:25} | {data['correct']:7d} | {data['incorrect']:9d} | {accuracy:10.1%} {perf_icon}")

            print("\n🎯 Overall AI Performance Summary:")
            if total_predictions > 0:
                overall_accuracy = total_correct / total_predictions
                print(f"  Total Human-Verified Predictions: {total_predictions}")
                print(f"  Correct AI Predictions:           {total_correct}")
                print(f"  Incorrect AI Predictions:         {total_incorrect}")
                print(f"  True AI Accuracy:                 {overall_accuracy:.1%}")
            else:
                print("  No data to calculate overall accuracy.")

        except Exception as e:
            print(f"❌ Error analyzing real-world performance: {e}")
    
    def generate_full_report(self):
        """Generate comprehensive evaluation report"""
        print("🚀 FOUNTAIN BUDDY MODEL EVALUATION DASHBOARD")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Load training history
        history = self.load_training_history()
        
        if not history:
            print("❌ No training history found. Run training first.")
            return
        
        # Run all analyses
        self.analyze_improvement_trends(history)
        self.analyze_species_performance(history)
        self.analyze_confidence_calibration(history)
        self.analyze_real_world_performance()
        
        print("\n✅ Evaluation complete!")
        print("\n💡 Recommendations:")
        if len(history) >= 2:
            latest_accuracy = history[-1]['best_val_accuracy']
            prev_accuracy = history[-2]['best_val_accuracy']
            if latest_accuracy > prev_accuracy:
                print("  🎉 Model is improving! Keep collecting corrections.")
            else:
                print("  🔄 Consider reviewing recent corrections for quality.")
        print("  📈 Focus corrections on species with <80% accuracy")
        print("  🎯 Aim for well-calibrated confidence (high confidence = high accuracy)")

def main():
    dashboard = ModelEvaluationDashboard()
    dashboard.generate_full_report()

if __name__ == "__main__":
    main()