import logging
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_swarm
from minimal.state import OrderState
from special_logger import loggy
from minimal.agents import (
    sales_agent,
    checkout_agent
)

logger = logging.getLogger(__name__)

# Build and compile the swarm with checkpointer
# Even though Studio says it's not necessary, let's try it to ensure state persistence
checkpointer = InMemorySaver()
builder = create_swarm(
    [sales_agent, checkout_agent],
    default_active_agent="sales_agent",
    state_schema=OrderState,
)
loggy.info("Building an app")
# loggy.info(f"State type: {type(OrderState)}, State attributes: {dir(OrderState)}")
app = builder.compile()


