from collections import deque

class WindowReading:
    """Represents a single reading in the sliding window."""
    def __init__(self, value: float, timestamp: float):
        self.value = value
        self.timestamp = timestamp

class SlidingWindow:
    """
    Manages a time-based sliding window of readings with efficient average calculations.
    
    Attributes:
        window_time: The time duration of the sliding window in seconds
        window: Double-ended queue storing the readings
        window_sum: Running sum of all values in the window
    """
    
    def __init__(self, window_time):
        """
        Initialize a new sliding window.
        
        Args:
            window_time: The time duration to maintain readings for (in seconds)
        """
        self.window_time = window_time
        self.window = deque()
        self.window_sum = 0.0
        
    def add_reading(self, value, timestamp):
        """
        Add a new reading to the window.
        
        Args:
            value: The value to add
            timestamp: The timestamp of the reading
        """
        reading = WindowReading(value, timestamp)
        self.window.appendleft(reading)
        self.window_sum += value
        
    def cleanup_old_readings(self, current_time):
        """
        Remove readings that are older than the window time.
        
        Args:
            current_time: The current timestamp to compare against
        """
        while self.window and (current_time - self.window[-1].timestamp) > self.window_time:
            old_reading = self.window.pop()
            self.window_sum -= old_reading.value
            
    def add(self, value, current_time):
        """
        Convenience method to add a new reading and cleanup old ones in one call.
        
        Args:
            value: The new value to add
            current_time: The current timestamp
        """
        self.add_reading(value, current_time)
        self.cleanup_old_readings(current_time)
        
    def avg(self):
        """
        Calculate the average of all values in the window.
        
        Returns:
            The average value, or 0 if the window is empty
        """
        if not self.window:
            return 0.0
        return self.window_sum / len(self.window)
    
    def get_latest_reading(self):
        """
        Get the most recent reading.
        
        Returns:
            The most recent reading, or None if window is empty
        """
        return self.window[0] if self.window else None
    
    def get_oldest_reading(self):
        """
        Get the oldest reading still in the window.
        
        Returns:
            The oldest reading, or None if window is empty
        """
        return self.window[-1] if self.window else None
    
    def __len__(self):
        """
        Get the number of readings currently in the window.
        
        Returns:
            Number of readings
        """
        return len(self.window)
    
    def clear(self):
        """Clear all readings from the window."""
        self.window.clear()
        self.window_sum = 0.0
    
