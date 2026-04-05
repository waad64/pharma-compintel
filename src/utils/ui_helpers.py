"""UI helper utilities"""

from typing import Optional

class UIHelper:
    """UI/UX helper functions"""
    
    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format number for display"""
        if value is None or (isinstance(value, float) and value != value):  # NaN check
            return "N/A"
        
        try:
            value = float(value)
            if value >= 1e9:
                return f"${value/1e9:.{decimals}f}B"
            elif value >= 1e6:
                return f"${value/1e6:.{decimals}f}M"
            elif value >= 1e3:
                return f"${value/1e3:.{decimals}f}K"
            return f"${value:.{decimals}f}"
        except (ValueError, TypeError):
            return "N/A"
    
    @staticmethod
    def get_status_color(status: str) -> str:
        """Get color for status badge"""
        status_colors = {
            'RECRUITING': '#48bb78',
            'COMPLETED': '#667eea',
            'ACTIVE_NOT_RECRUITING': '#ed8936',
            'TERMINATED': '#f56565',
            'ACTIVE': '#48bb78',
            'INACTIVE': '#cbd5e0'
        }
        return status_colors.get(status, '#cbd5e0')
    
    @staticmethod
    def get_status_emoji(status: str) -> str:
        """Get emoji for status"""
        status_emojis = {
            'RECRUITING': '🔍',
            'COMPLETED': '✓',
            'ACTIVE_NOT_RECRUITING': '⏸',
            'TERMINATED': '✗',
            'ACTIVE': '▶',
            'INACTIVE': '⏹'
        }
        return status_emojis.get(status, '•')
    
    @staticmethod
    def format_date(date_obj) -> str:
        """Format date for display"""
        if date_obj is None:
            return "N/A"
        try:
            return date_obj.strftime('%Y-%m-%d')
        except:
            return str(date_obj)
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """Format percentage for display"""
        if value is None:
            return "N/A"
        try:
            return f"{float(value):.{decimals}f}%"
        except (ValueError, TypeError):
            return "N/A"
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 50) -> str:
        """Truncate text with ellipsis"""
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text
    
    @staticmethod
    def format_list(items: list, separator: str = ", ", max_items: int = 3) -> str:
        """Format list for display"""
        if not items:
            return "N/A"
        if len(items) > max_items:
            return separator.join(str(i) for i in items[:max_items]) + f" +{len(items)-max_items} more"
        return separator.join(str(i) for i in items)

class MetricsCollector:
    """Collect and aggregate metrics"""
    
    @staticmethod
    def calculate_growth(current: float, previous: float) -> float:
        """Calculate growth percentage"""
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def get_trend_indicator(value: float) -> str:
        """Get trend indicator emoji"""
        if value > 0:
            return "📈"
        elif value < 0:
            return "📉"
        return "➡️"
    
    @staticmethod
    def get_trend_color(value: float) -> str:
        """Get trend color"""
        if value > 0:
            return "#48bb78"  # Green
        elif value < 0:
            return "#f56565"  # Red
        return "#718096"  # Gray
