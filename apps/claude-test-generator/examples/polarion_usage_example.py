#!/usr/bin/env python3
"""
Polarion Integration Usage Example
Demonstrates how to use Polarion integration with Claude Test Generator
"""

import os
import json
import sys
from pathlib import Path

# Add polarion module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from polarion import PolarionConfig, TestCaseFetcher, TestCasePoster

def example_setup_and_test():
    """Example: Setup and test Polarion connection"""
    print("🔧 Setting up Polarion configuration...")
    
    # Create configuration
    config = PolarionConfig()
    
    # Check if configuration is valid
    is_valid, errors = config.validate()
    if not is_valid:
        print("❌ Configuration invalid:")
        for error in errors:
            print(f"   - {error}")
        print("\n💡 Set environment variables:")
        print("   export POLARION_PAT_TOKEN='your-token'")
        print("   export POLARION_URL='https://polarion.company.com'")
        print("   export POLARION_PROJECT_ID='PROJECT_ID'")
        return False
    
    print("✅ Configuration valid")
    
    # Test connection
    try:
        from polarion.api_client import PolarionAPIClient
        auth_config = config.get_authentication_config()
        client = PolarionAPIClient(**auth_config)
        
        if client.health_check():
            print("✅ Polarion connection successful")
            return True
        else:
            print("❌ Polarion connection failed")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def example_fetch_learning_data():
    """Example: Fetch test cases for learning"""
    print("\n📚 Fetching learning data from Polarion...")
    
    try:
        config = PolarionConfig()
        fetcher = TestCaseFetcher(config)
        
        # Fetch learning samples
        learning_data = fetcher.fetch_learning_samples(
            search_terms=['ACM', 'OpenShift', 'cluster'],
            limit=10  # Small limit for example
        )
        
        # Print summary
        stats = learning_data.get('statistics', {})
        patterns = learning_data.get('patterns', {})
        insights = learning_data.get('learning_insights', {})
        
        print(f"✅ Fetched {stats.get('total_count', 0)} test cases")
        print(f"📊 Average steps per test: {stats.get('avg_step_count', 0):.1f}")
        
        if patterns.get('common_validation_approaches'):
            top_validations = list(patterns['common_validation_approaches'].keys())[:3]
            print(f"🔍 Top validation approaches: {', '.join(top_validations)}")
        
        if insights.get('validation_best_practices'):
            print(f"💡 Best practices: {', '.join(insights['validation_best_practices'])}")
        
        # Save learning data
        output_file = "example_learning_data.json"
        if fetcher.save_learning_data(learning_data, output_file):
            print(f"💾 Learning data saved to: {output_file}")
        
        return learning_data
        
    except Exception as e:
        print(f"❌ Failed to fetch learning data: {e}")
        return None

def example_create_sample_test_case():
    """Example: Create a sample test case for posting"""
    print("\n📝 Creating sample test case...")
    
    sample_test_case = {
        'title': 'Example ACM Cluster Import Validation',
        'description': 'Validates the import process for a managed cluster in ACM',
        'setup': 'Access to ACM hub cluster and a cluster ready for import',
        'test_steps': [
            {
                'step': '**Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify`',
                'expected_result': 'Login successful with access confirmed:\n```\nLogin successful.\nYou have access to 67 projects\n```'
            },
            {
                'step': '**Step 2: Create import YAML** - Create managed cluster import configuration: `oc apply -f import-cluster.yaml`',
                'expected_result': 'Import configuration created successfully:\n```\nmanagedcluster.cluster.open-cluster-management.io/test-cluster created\n```'
            },
            {
                'step': '**Step 3: Verify cluster import** - Check cluster status: `oc get managedclusters`',
                'expected_result': 'Cluster appears in managed clusters list:\n```\nNAME          HUB ACCEPTED   JOINED   AVAILABLE\ntest-cluster  true           True     True\n```'
            }
        ]
    }
    
    # Save as markdown file for posting example
    markdown_content = f"""# Example Test Cases for Polarion

## Test Case 1: {sample_test_case['title']}

**Description:** {sample_test_case['description']}

**Setup:** {sample_test_case['setup']}

| Step | Expected Result |
|------|-----------------|
"""
    
    for step_data in sample_test_case['test_steps']:
        markdown_content += f"| {step_data['step']} | {step_data['expected_result']} |\n"
    
    output_file = "example_test_case.md"
    with open(output_file, 'w') as f:
        f.write(markdown_content)
    
    print(f"✅ Sample test case created: {output_file}")
    return output_file, sample_test_case

def example_post_test_case(markdown_file, test_case_data):
    """Example: Post test case to Polarion"""
    print(f"\n📤 Posting test case to Polarion...")
    
    try:
        config = PolarionConfig()
        poster = TestCasePoster(config)
        
        project_id = config.get('default_project_id')
        if not project_id:
            print("❌ No project ID configured")
            return False
        
        print(f"📋 Posting to project: {project_id}")
        
        # Post the test case
        created_ids = poster.post_test_cases_from_markdown(
            markdown_file=markdown_file,
            project_id=project_id,
            metadata={
                'status': 'draft',
                'priority': 'normal',
                'severity': 'normal'
            }
        )
        
        if created_ids:
            print(f"✅ Successfully posted {len(created_ids)} test cases:")
            for test_id in created_ids:
                print(f"   - {test_id}")
            
            # Generate report
            results = {
                'total_attempted': len(created_ids),
                'successful': [{'id': tid, 'title': f'Example Test Case'} for tid in created_ids],
                'failed': [],
                'errors': [],
                'success_rate': 1.0
            }
            
            report_content = poster.generate_posting_report(results)
            
            report_file = "example_posting_report.md"
            with open(report_file, 'w') as f:
                f.write(report_content)
            
            print(f"📋 Report saved to: {report_file}")
            return True
        else:
            print("❌ No test cases were posted")
            return False
            
    except Exception as e:
        print(f"❌ Failed to post test case: {e}")
        return False

def main():
    """Main example function"""
    print("🚀 Polarion Integration Example")
    print("=" * 50)
    
    # 1. Setup and test connection
    if not example_setup_and_test():
        print("\n❌ Setup failed. Please configure Polarion connection first.")
        return 1
    
    # 2. Fetch learning data
    learning_data = example_fetch_learning_data()
    
    # 3. Create sample test case
    markdown_file, test_case_data = example_create_sample_test_case()
    
    # 4. Post test case (commented out by default to avoid accidentally posting)
    print(f"\n📤 Ready to post test case to Polarion")
    print(f"📁 Markdown file: {markdown_file}")
    print("\n💡 To actually post the test case, uncomment the posting code below")
    print("⚠️ This will create a real test case in Polarion!")
    
    # Uncomment the following lines to actually post to Polarion:
    # success = example_post_test_case(markdown_file, test_case_data)
    # if success:
    #     print("\n🎉 Example completed successfully!")
    # else:
    #     print("\n❌ Posting failed")
    
    print("\n✅ Example demonstration completed")
    print("\nGenerated files:")
    print(f"   - {markdown_file}")
    if learning_data:
        print(f"   - example_learning_data.json")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
