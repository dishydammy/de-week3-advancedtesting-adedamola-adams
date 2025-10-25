import pytest
from order_pipeline.analyzer import DataAnalyzer

@pytest.fixture
def analyzer():
    """Returns a DataAnalyzer instance."""
    return DataAnalyzer()

@pytest.fixture
def transformed_data():
    """Provides sample transformed data for analysis."""
    return [
        {
            "order_id": "ORD100", "item": "Laptop", "quantity": 1, "price": 1200.00,
            "payment_status": "paid", "total": 1200.00
        },
        {
            "order_id": "ORD101", "item": "Mouse", "quantity": 2, "price": 20.00,
            "payment_status": "paid", "total": 40.00
        },
        {
            "order_id": "ORD102", "item": "Keyboard", "quantity": 1, "price": 50.00,
            "payment_status": "pending", "total": 50.00
        },
        {
            "order_id": "ORD103", "item": "Monitor", "quantity": 1, "price": 300.00,
            "payment_status": "pending", "total": 300.00
        },
        {
            "order_id": "ORD104", "item": "USB Hub", "quantity": 1, "price": 25.00,
            "payment_status": "refunded", "total": 25.00
        },
        {
            "order_id": "ORD105", "item": "Cable", "quantity": 3, "price": 10.00,
            "payment_status": "paid", "total": 30.00
        },
    ]

class TestDataAnalyzer:

    def test_analyze_data(self, analyzer, transformed_data):
        """Tests the main analysis logic."""
        analysis = analyzer.analyze_data(transformed_data)
        
        # Total Revenue = 1200.00 (ORD100) + 40.00 (ORD101) + 30.00 (ORD105)
        assert analysis["total_revenue"] == 1270.00
        
        # Total Orders = 6
        assert analysis["total_orders"] == 6
        
        # Average Revenue = 1270.00 / 6
        assert analysis["average_revenue"] == pytest.approx(1270.00 / 6)
        
        # Status Counts
        assert analysis["status_counts"]["paid"] == 3
        assert analysis["status_counts"]["pending"] == 2
        assert analysis["status_counts"]["refunded"] == 1

    def test_empty_input(self, analyzer):
        """Tests analysis on an empty data list."""
        analysis = analyzer.analyze_data([])
        
        assert analysis["total_revenue"] == 0
        assert analysis["average_revenue"] == 0
        assert analysis["total_orders"] == 0
        assert analysis["status_counts"]["paid"] == 0
        assert analysis["status_counts"]["pending"] == 0
        assert analysis["status_counts"]["refunded"] == 0

    def test_no_paid_orders(self, analyzer, transformed_data):
        """Tests analysis when no orders have 'paid' status."""
        no_paid_data = [
            r for r in transformed_data if r["payment_status"] != "paid"
        ]
        # This will include 2 pending, 1 refunded
        analysis = analyzer.analyze_data(no_paid_data)
        
        assert analysis["total_revenue"] == 0
        assert analysis["total_orders"] == 3
        assert analysis["average_revenue"] == 0
        assert analysis["status_counts"]["paid"] == 0
        assert analysis["status_counts"]["pending"] == 2
        assert analysis["status_counts"]["refunded"] == 1

    def test_all_paid_orders(self, analyzer, transformed_data):
        """Tests analysis when all orders are 'paid'."""
        all_paid_data = [
            r for r in transformed_data if r["payment_status"] == "paid"
        ]
        # Total revenue = 1270.00, Total orders = 3
        analysis = analyzer.analyze_data(all_paid_data)
        
        assert analysis["total_revenue"] == 1270.00
        assert analysis["total_orders"] == 3
        assert analysis["average_revenue"] == pytest.approx(1270.00 / 3)
        assert analysis["status_counts"]["paid"] == 3
        assert analysis["status_counts"]["pending"] == 0
        assert analysis["status_counts"]["refunded"] == 0
