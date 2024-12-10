from SUPABASE.create_client import get_client
from supabase import PostgrestAPIResponse


def select(
        table: str,
        columns: str = '*',
        filters: dict = None,
        limit: int = None,
        order: str = None,
        desc: bool = False,
        count: bool = False
) -> PostgrestAPIResponse:
    """
    Perform a select operation on a Supabase table with optional filtering, ordering, and counting.

    Args:
        table (str): Name of the table to query.
        columns (str): Columns to select, default is '*'.
        filters (dict): A dictionary of filters to apply to the query. Operators such as 'gte', 'lt', etc. can be included.
        limit (int): Limit the number of results.
        order (str): The column to order by.
        desc (bool): Whether to order by descending or not.
        count (bool): If True, perform a count instead of returning data.

    Returns:
        PostgrestAPIResponse: The result of the query.
    """
    if filters is None:
        filters = {}

    client = get_client()

    # If counting rows is requested
    if count:
        query = client.table(table).select(columns, count="exact")
    else:
        query = client.table(table).select(columns)

    if filters is None:
        filters = {}

    # Apply filters
    for key, value in filters.items():
        if isinstance(value, dict):  # Check if it's a range or condition
            for op, val in value.items():
                if op in ('>=', 'gte'):
                    query = query.gte(key, val)
                elif op in ('>', 'gt'):
                    query = query.gt(key, val)
                elif op in ('<=', 'lte'):
                    query = query.lte(key, val)
                elif op in ('<', 'lt'):
                    query = query.lt(key, val)
                else:
                    raise ValueError(f"Unsupported operator {op}")
        else:
            query = query.eq(key, value)  # Default equality filter

    # Apply ordering if specified
    if order:
        query = query.order(order, desc=desc)

    # Apply limit if specified
    if limit:
        query = query.limit(limit)

    result = query.execute()

    # Execute and return the query result
    return result


