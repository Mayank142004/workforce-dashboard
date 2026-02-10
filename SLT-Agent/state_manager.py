from datetime import date


class DailyState:
    """
    Holds per-day working state.
    This is the SINGLE SOURCE OF TRUTH for:
    - Working seconds
    - Idle/lunch/break usage
    - First activity (IN)
    - Last activity (OUT)
    """

    def __init__(self):
        self.reset()

    def reset(self):
        # ------------------------------
        # Day boundary (STRICT)
        # ------------------------------
        self.date = date.today()

        # ------------------------------
        # Work counters (seconds)
        # ------------------------------
        self.normal_seconds = 0      # Max 8 hours
        self.ot_seconds = 0          # Max 4 hours

        # ------------------------------
        # Idle / break tracking
        # ------------------------------
        self.lunch_used = False      # 1 × 60 min
        self.breaks_used = 0         # 2 × 15 min

        # ------------------------------
        # REAL activity timing
        # ------------------------------
        # First keyboard/mouse activity of the day
        self.first_seen = None

        # Last ACTIVE (non-idle) activity time
        # ⚠️ Updated ONLY when idle < threshold
        self.last_seen = None

    # ------------------------------------------------
    # Helpers (safe, optional but useful)
    # ------------------------------------------------
    def has_started(self):
        """Returns True if employee has started work today"""
        return self.first_seen is not None

    def has_activity(self):
        """Returns True if any working seconds exist"""
        return (self.normal_seconds + self.ot_seconds) > 0

    def total_work_seconds(self):
        """Total payable work time"""
        return self.normal_seconds + self.ot_seconds
