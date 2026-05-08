"""
GreenAI Data Utilities
CSV export/import functions for persistence
"""

import os
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class DataExporter:
    """Handle CSV exports and imports"""
    
    def __init__(self, output_dir: str = 'outputs'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_observations(self, observations: List[Dict], filename: Optional[str] = None) -> str:
        """Export observations list to CSV"""
        
        if not observations:
            print("⚠️ No observations to export")
            return None
        
        df = pd.DataFrame(observations)
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'observations_{timestamp}.csv'
        
        filepath = self.output_dir / filename
        df.to_csv(filepath, index=False)
        
        print(f"✅ Exported {len(observations)} observations to {filepath}")
        return str(filepath)
    
    def export_results(self, results_df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """Export experiment results to CSV"""
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'results_{timestamp}.csv'
        
        filepath = self.output_dir / filename
        results_df.to_csv(filepath, index=False)
        
        print(f"✅ Exported {len(results_df)} results to {filepath}")
        return str(filepath)
    
    def export_statistics(self, stats: List[Dict], filename: Optional[str] = None) -> str:
        """Export model statistics to CSV"""
        
        if not stats:
            print("⚠️ No statistics to export")
            return None
        
        df = pd.DataFrame(stats)
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'statistics_{timestamp}.csv'
        
        filepath = self.output_dir / filename
        df.to_csv(filepath, index=False)
        
        print(f"✅ Exported {len(stats)} statistics to {filepath}")
        return str(filepath)
    
    def export_routing_history(self, history: List[Dict], filename: Optional[str] = None) -> str:
        """Export router selection history to CSV"""
        
        if not history:
            print("⚠️ No routing history to export")
            return None
        
        df = pd.DataFrame(history)
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'routing_history_{timestamp}.csv'
        
        filepath = self.output_dir / filename
        df.to_csv(filepath, index=False)
        
        print(f"✅ Exported {len(history)} routing decisions to {filepath}")
        return str(filepath)


class DataLoader:
    """Load CSV files for analysis"""
    
    @staticmethod
    def load_observations(filepath: str) -> pd.DataFrame:
        """Load observations from CSV"""
        
        if not os.path.exists(filepath):
            print(f"⚠️ File not found: {filepath}")
            return pd.DataFrame()
        
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} observations from {filepath}")
        return df
    
    @staticmethod
    def load_results(filepath: str) -> pd.DataFrame:
        """Load results from CSV"""
        
        if not os.path.exists(filepath):
            print(f"⚠️ File not found: {filepath}")
            return pd.DataFrame()
        
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} results from {filepath}")
        return df
    
    @staticmethod
    def load_statistics(filepath: str) -> pd.DataFrame:
        """Load statistics from CSV"""
        
        if not os.path.exists(filepath):
            print(f"⚠️ File not found: {filepath}")
            return pd.DataFrame()
        
        df = pd.read_csv(filepath)
        print(f"✅ Loaded statistics from {filepath}")
        return df
    
    @staticmethod
    def load_routing_history(filepath: str) -> pd.DataFrame:
        """Load routing history from CSV"""
        
        if not os.path.exists(filepath):
            print(f"⚠️ File not found: {filepath}")
            return pd.DataFrame()
        
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} routing decisions from {filepath}")
        return df
    
    @staticmethod
    def find_latest_file(directory: str, pattern: str) -> Optional[str]:
        """Find the most recent CSV file matching pattern"""
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return None
        
        matching_files = list(dir_path.glob(f"{pattern}_*.csv"))
        
        if not matching_files:
            return None
        
        # Sort by modification time, get most recent
        latest = max(matching_files, key=lambda p: p.stat().st_mtime)
        return str(latest)


class DataAggregator:
    """Aggregate and summarize data"""
    
    @staticmethod
    def aggregate_by_model(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate metrics by model"""
        
        if df.empty:
            return pd.DataFrame()
        
        agg = df.groupby('model').agg({
            'quality_score': ['mean', 'std', 'count'],
            'carbon_g': ['mean', 'std'],
            'latency': ['mean', 'std'],
            'total_tokens': ['mean', 'sum'],
            'greenai_score': 'mean',
            'energy_kwh': 'sum'
        }).round(4)
        
        return agg
    
    @staticmethod
    def aggregate_by_task_type(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate metrics by task type"""
        
        if df.empty:
            return pd.DataFrame()
        
        agg = df.groupby('task_type').agg({
            'quality_score': ['mean', 'std'],
            'carbon_g': ['mean', 'std'],
            'latency': ['mean', 'std'],
            'greenai_score': 'mean',
            'total_tokens': ['mean', 'count']
        }).round(4)
        
        return agg
    
    @staticmethod
    def get_summary_stats(df: pd.DataFrame) -> Dict:
        """Get overall summary statistics"""
        
        if df.empty:
            return {}
        
        return {
            'total_requests': len(df),
            'avg_quality': df['quality_score'].mean(),
            'avg_carbon': df['carbon_g'].mean(),
            'avg_latency': df['latency'].mean(),
            'avg_greenai_score': df['greenai_score'].mean(),
            'total_carbon': df['carbon_g'].sum(),
            'total_energy_kwh': df['energy_kwh'].sum(),
            'total_tokens': df['total_tokens'].sum(),
            'num_models': df['model'].nunique(),
            'num_task_types': df['task_type'].nunique()
        }


if __name__ == '__main__':
    # Test the utilities
    print("GreenAI Data Utilities Test")
    print("=" * 60)
    
    # Create sample data
    sample_data = [
        {
            'timestamp': datetime.now().isoformat(),
            'model': 'agent_fast',
            'task_id': 'qa_001',
            'task_type': 'qa',
            'prompt': 'What is 2+2?',
            'response': '4',
            'input_tokens': 5,
            'output_tokens': 2,
            'total_tokens': 7,
            'latency': 0.5,
            'quality_score': 0.95,
            'carbon_g': 0.001,
            'energy_kwh': 0.0000035,
            'greenai_score': 85.5
        },
        {
            'timestamp': datetime.now().isoformat(),
            'model': 'agent_balanced',
            'task_id': 'qa_002',
            'task_type': 'qa',
            'prompt': 'What is 2+2?',
            'response': '2+2 equals 4',
            'input_tokens': 5,
            'output_tokens': 5,
            'total_tokens': 10,
            'latency': 1.0,
            'quality_score': 1.0,
            'carbon_g': 0.0015,
            'energy_kwh': 0.0000050,
            'greenai_score': 90.0
        }
    ]
    
    # Test export
    exporter = DataExporter('outputs')
    exporter.export_observations(sample_data, 'test_observations.csv')
    
    # Test load
    loader = DataLoader()
    df = loader.load_observations('outputs/test_observations.csv')
    print(f"\n✅ Loaded dataframe shape: {df.shape}")
    
    # Test aggregation
    agg = DataAggregator.aggregate_by_model(df)
    print(f"\n📊 Aggregated by model:\n{agg}")
    
    summary = DataAggregator.get_summary_stats(df)
    print(f"\n📈 Summary stats:\n{summary}")
