from typing import List, Dict, Any

class DataAnalyzer:
    """Computes statistics from transformed order data."""

    def analyze_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Computes summary statistics for the cleaned data."""
        if not data:
            return {
                "total_revenue": 0,
                "average_revenue": 0,
                "total_orders": 0,
                "status_counts": {
                    "paid": 0,
                    "pending": 0,
                    "refunded": 0
                }
            }

        total_revenue = 0.0
        status_counts = {"paid": 0, "pending": 0, "refunded": 0}
        
        for record in data:
            status = record.get('payment_status', 'pending')
            
            if status == 'paid':
                total_revenue += record.get('total', 0.0)
            
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts['pending'] += 1
        
        total_orders = len(data)
        average_revenue = (total_revenue / total_orders) if total_orders > 0 else 0

        return {
            "total_revenue": round(total_revenue, 2),
            "average_revenue": average_revenue,
            "total_orders": total_orders,
            "status_counts": status_counts
        }

