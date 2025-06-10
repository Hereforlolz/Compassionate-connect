from onboarding_coordinator_agent import OnboardingCoordinatorAgent

if __name__ == "__main__":
    api_key = "YOUR_KEY"  # Replace with your actual key
    coordinator = OnboardingCoordinatorAgent("compassionate-connect-ai", api_key)
    coordinator.run()
