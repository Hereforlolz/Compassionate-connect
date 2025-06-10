# coordinator_agent.py
import os
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic

class OnboardingCoordinatorAgent:
    def __init__(self, project_id):
        """Initialize the Coordinator Agent"""
        self.project_id = project_id
        self.location = "us-central1"  # Google Cloud region
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=self.location)
        
        print("🤖 OnboardingCoordinatorAgent initialized!")
        print("Ready to help patients with their mental health onboarding.")
    
    def welcome_patient(self):
        """Welcome the patient and explain the process"""
        welcome_message = """
        🌟 Welcome to CompassionateConnect AI! 🌟
        
        I'm here to help make your mental health care onboarding as smooth and comfortable as possible.
        
        Here's what we'll do together:
        1. I'll ask you some basic questions about yourself
        2. We'll do a brief, gentle mental health assessment
        3. If you need immediate support, I can connect you with crisis resources
        4. All your information will be stored securely for your care team
        
        Everything is confidential and at your own pace. You can stop anytime.
        
        Are you ready to begin? (Type 'yes' to continue or 'help' for more information)
        """
        
        print(welcome_message)
        return welcome_message
    
    def get_patient_response(self):
        """Get input from the patient"""
        response = input("\nYour response: ").strip().lower()
        return response
    
    def process_initial_response(self, response):
        """Process the patient's initial response"""
        if response in ['yes', 'y', 'ready', 'ok']:
            print("\n✅ Wonderful! Let's begin your onboarding process.")
            return "ready_to_start"
        
        elif response in ['help', 'h', 'more info']:
            help_message = """
            📋 More Information:
            
            • This process typically takes 10-15 minutes
            • We ask about basic information (name, contact info)
            • We'll ask some gentle questions about how you're feeling
            • Your privacy is completely protected
            • A human counselor will review everything later
            • If you're in crisis, I can immediately connect you with help
            
            Would you like to start now? (Type 'yes' when ready)
            """
            print(help_message)
            return "needs_more_info"
        
        elif response in ['no', 'n', 'not ready', 'stop']:
            print("\n🤗 That's completely okay! Take your time.")
            print("When you're ready, just restart this process.")
            return "not_ready"
        
        else:
            print("\n❓ I didn't quite understand that.")
            print("Please type 'yes' to begin, 'help' for more info, or 'no' if you're not ready.")
            return "unclear_response"

# Simple test function
def test_coordinator():
    """Test the coordinator agent"""
    print("Testing OnboardingCoordinatorAgent...")
    
    # You'll need to replace this with your actual project ID
    # You can find it in Google Cloud Console
    project_id = "compassionate-connect-ai"  # Replace with your actual project ID
    
    try:
        # Create the agent
        coordinator = OnboardingCoordinatorAgent(project_id)
        
        # Start the welcome process
        coordinator.welcome_patient()
        
        # Simple interaction loop
        while True:
            response = coordinator.get_patient_response()
            result = coordinator.process_initial_response(response)
            
            if result == "ready_to_start":
                print("\n🎉 Great! In our next step, we'll connect this to the intake questionnaire agent.")
                break
            elif result == "not_ready":
                break
            elif result in ["needs_more_info", "unclear_response"]:
                continue  # Keep asking
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your Google Cloud project ID is correct!")

if __name__ == "__main__":
    test_coordinator()