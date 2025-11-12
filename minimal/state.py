from typing import Optional
from langgraph_swarm import SwarmState
from langchain_core.runnables import RunnableConfig

class OrderState(SwarmState, total=False):
    """State schema for the order entry system."""
    order_items: Optional[list[dict]]
    order_total: Optional[float]
    customer_name: Optional[str]
    customer_email: Optional[str]
    # Required by create_react_agent when using custom state_schema
    remaining_steps: Optional[int]


# Context reducers for different agents
def order_context_reducer(state: dict, config: RunnableConfig) -> str:
    """Reducer for sales agent - shows order items and total only."""
    order_items = state.get("order_items", [])
    order_total = state.get("order_total", 0.0)
    
    if not order_items:
        return "Current Order: Empty\nTotal: $0.00"
    
    items_text = "\n".join([
        f"  - {item['quantity']}x {item['name']} @ ${item['price']:.2f} = ${item['total']:.2f}"
        for item in order_items
    ])
    
    return f"""Current Order:
{items_text}
Total: ${order_total:.2f}"""


def full_context_reducer(state: dict, config: RunnableConfig) -> str:
    """Reducer for checkout agent - shows everything including customer info."""
    order_items = state.get("order_items", [])
    order_total = state.get("order_total", 0.0)
    customer_name = state.get("customer_name", "Not provided")
    customer_email = state.get("customer_email", "Not provided")
    
    items_text = "\n".join([
        f"  - {item['quantity']}x {item['name']} @ ${item['price']:.2f}"
        for item in order_items
    ]) if order_items else "  (none)"
    
    return f"""Customer: {customer_name}
Email: {customer_email}
Order Items:
{items_text}
Order Total: ${order_total:.2f}"""