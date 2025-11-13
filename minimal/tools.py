import logging
from typing import Annotated, Any
from langgraph.prebuilt import InjectedState
from langchain_core.tools import InjectedToolCallId, tool
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from special_logger import loggy

# Order management tools
@tool
def add_to_order(
    item_name: str,
    quantity: int,
    price: float,
    state: Annotated[Any, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Add an item to the customer's order.
    
    Args:
        item_name: Name of the item to add
        quantity: Number of items to add
        price: Price per item
    """
    
    loggy.info(f"State type: {type(state)}. State keys: {list(state.keys())}")
    current_items = state.get("order_items", [])
    current_total = state.get("order_total", 0.0)
    
    new_item = {
        "name": item_name,
        "quantity": quantity,
        "price": price,
        "total": quantity * price
    }
    
    updated_items = current_items + [new_item]
    updated_total = current_total + (quantity * price)
    
    message = ToolMessage(content=f"Added Item {item_name} with quantity {quantity} and price {price}", tool_call_id=tool_call_id)
    update = {
        "order_items": updated_items,
        "order_total": updated_total,
        "messages": [message]
    }
    return Command(update=update)


@tool
def remove_from_order(
    item_name: str,
    state: Annotated[Any, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Remove an item from the customer's order.
    
    Args:
        item_name: Name of the item to remove
    """
    current_items = state.get("order_items", [])
    current_total = state.get("order_total", 0.0)
    
    # Find and remove item
    updated_items = [item for item in current_items if item["name"] != item_name]
    removed_items = [item for item in current_items if item["name"] == item_name]
    
    removed_total = sum(item["total"] for item in removed_items)
    
    message = ToolMessage(content=f"removed item {item_name} from order", tool_call_id=tool_call_id)
    update = {
        "order_items": updated_items,
        "order_total": current_total - removed_total,
        "messages": [message]
    }
    return Command(update=update)
    


@tool
def update_customer_info(
    name: str,
    email: str,
    state: Annotated[Any, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Update customer information.
    
    Args:
        name: Customer's name
        email: Customer's email address
    """
    try:
        loggy.info(f"State type: {type(state)}")
        message = ToolMessage(content=f"updated customer info with {name} and {email}", tool_call_id=tool_call_id)
        update = {
            "customer_name": name,
            "customer_email": email,
            "messages": [message]
        }
        return Command(update=update)
    except Exception as e:
        # Ensure we always return a Command with ToolMessage, even on error
        error_message = ToolMessage(content=f"Error updating customer info: {str(e)}", tool_call_id=tool_call_id)
        return Command(update={"messages": [error_message]})


@tool
def finalize_order(
    state: Annotated[Any, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Finalize and submit the order for processing.
    
    This tool completes the order and should only be called when:
    - All items are confirmed
    - Customer information is complete
    - Customer has approved the order
    """
    loggy.info(f"State type right before order is finalized: {type(state)}")
    loggy.info(f"State right before order is finalized: {state}")
    order_items = state.get("order_items", [])
    customer_name = state.get("customer_name", "")
    if not order_items:
        error_message = ToolMessage(content="Error: Cannot finalize an empty order.", tool_call_id=tool_call_id)
        return Command(update={"messages": [error_message]})
    
    if not customer_name:
        error_message = ToolMessage(content="Error: Customer name is required before finalizing.", tool_call_id=tool_call_id)
        loggy.info(f"State right after the order is determined to be empty {state}")
        return Command(update={"messages": [error_message]})
    
    message = ToolMessage(content=f"Successfully placed order", tool_call_id=tool_call_id)
    update = {
        "customer_name": "",
        "customer_email": "",
        "order_items": [],
        "order_total": 0.0,
        "messages": [message]
    }
    return Command(update=update)