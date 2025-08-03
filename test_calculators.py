"""
Calculator comparison tests using AskUI for UI automation.
Tests different calculator implementations to ensure consistent results.
"""

import abc
import logging
import subprocess
import pytest
from askui import VisionAgent
from askui.reporting import SimpleHtmlReporter

class Calculator(abc.ABC):
    """Base calculator class defining common interface."""
    
    def __init__(self, agent: VisionAgent):
        """Initialize calculator with AskUI agent.
        
        Args:
            agent: AskUI Vision Agent for UI interaction
        """
        self.agent = agent

    @abc.abstractmethod
    def open(self) -> None:
        """Open the calculator application."""
        pass

class WindowsCalculator(Calculator):
    """Windows Calculator implementation using native app."""
    
    def open(self) -> None:
        """Launch Windows Calculator application."""
        subprocess.Popen('calc.exe')
        self.agent.wait(2)  # Wait for calculator to initialize


class GoogleCalculator(Calculator):
    """Google Calculator implementation using web browser."""
    
    def open(self) -> None:
        """Navigate to Google and open calculator."""
        self.agent.tools.webbrowser.open_new("https://www.google.com")
        self.agent.wait(2)  # Wait for page load
        self.agent.type("calculator")
        self.agent.keyboard('enter')
        self.agent.wait(2)  # Wait for calculator to appear

@pytest.fixture(scope="module")
def agent() -> VisionAgent:
    """Provide configured AskUI Vision Agent.
    
    Returns:
        VisionAgent: Configured agent with HTML reporting
    """
    agent = VisionAgent(
        log_level=logging.DEBUG,
        reporters=[SimpleHtmlReporter()]
    )
    agent.open()
    yield agent
    agent.close()


@pytest.fixture(params=["windows", "google"])
def calculator(request, agent) -> Calculator:
    """Provide calculator instances for testing.
    
    Args:
        request: Pytest request object with parameters
        agent: AskUI Vision Agent
        
    Returns:
        Calculator: Configured calculator instance
    """
    if request.param == "windows":
        return WindowsCalculator(agent)
    return GoogleCalculator(agent)


def test_addition(calculator: Calculator) -> None:
    """Test addition functionality across different calculators.
    
    Verifies that 1 + 2 = 3 on both Windows and Google calculators.
    
    Args:
        calculator: Calculator instance to test
    """
    calculator.open()
    calculator.agent.act("Calculate 1 + 2 using the calculator on screen")
    result = calculator.agent.get("What is the number shown in the calculator's display?")
    assert float(result) == 3, f"Addition failed: expected 3, got {result}"
