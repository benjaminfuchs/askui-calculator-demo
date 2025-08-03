"""
Field Device Tool (FDT) Commissioning Tests.

This module contains automated tests for the FDT offline commissioning workflow,
specifically focusing on the pre-selection wizard process.
"""

import logging
import subprocess
from typing import Generator
import pytest
from askui import VisionAgent
from askui.reporting import SimpleHtmlReporter


class FdtHost:
    """FDT Frame Application interface wrapper."""
    
    def __init__(self, agent: VisionAgent):
        """Initialize FDT interface with AskUI agent.
        
        Args:
            agent: AskUI Vision Agent for UI interaction
        """
        self.agent = agent

    def check_navigation_menu(self, menu_name: str) -> bool:
        """Check if a specific menu is visible in the navigation area.
        
        Args:
            menu_name: Name of the menu to look for (e.g., 'Guidance', 'Configuration')
            
        Returns:
            bool: True if the specified menu is present, False otherwise
        """
        response = self.agent.get(
            f"Is there a {menu_name} menu visible in the navigation area? Answer 'yes' or 'no'."
        )
        return "yes" in response.lower()


@pytest.fixture(scope="module")
def agent() -> Generator[VisionAgent, None, None]:
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


@pytest.fixture
def fdt_host(agent) -> FdtHost:
    """Provide FDT interface instance for testing.
    
    Args:
        agent: AskUI Vision Agent
        
    Returns:
        FdtHost: Configured FDT interface instance
    """
    return FdtHost(agent)


def test_offline_preselection(fdt_host: FdtHost) -> None:
    """Test the offline pre-selection wizard workflow.
        
    Args:
        fdt_host: FDT Frame Application interface instance
    """

    assert not fdt_host.check_navigation_menu("Guidance"), (
        "Pre-selection wizard cannot be started - Guidance menu is already present"
    )

    # Start pre-selection wizard
    fdt_host.agent.act(
        "Open the pre-selection wizard by navigating through the menus or toolbar. "
        "Look for terms like 'Pre-selection', 'Device Setup', or 'Configuration'."
    )
    fdt_host.agent.wait(2)  # Wait for wizard to appear

    # Execute the wizard steps
    fdt_host.agent.act(
        "We will now complete the pre-selection wizard: "
        "1. For each parameter marked as 'Please select', choose the first reasonable option "
        "2. Confirm each selection with Enter "
        "3. Navigate through all steps using the 'Next' button until you see a 'Finish' button "
        "4. Click Finish when all parameters are set to close the wizard. "
        "Stay within the DTM window only"
        "Buttons may look like standard buttons or hyperlinks, do not click the close button."
    )
    
    # Verify successful completion
    fdt_host.agent.wait(2)  # Wait for wizard to close and UI to update
    assert fdt_host.check_navigation_menu("Guidance"), (
        "Pre-selection wizard did not complete successfully - Guidance menu not found"
    )
