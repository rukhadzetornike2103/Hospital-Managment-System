

class Room:
    class RoomType:
        SINGLE = "Single"
        DOUBLE = "Double"
        ICU = "ICU"

    def __init__(self, room_number, room_type, daily_rate):
        self._room_number = room_number
        self._room_type = room_type
        self._daily_rate = daily_rate
        self._capacity = 2 if room_type == self.RoomType.DOUBLE else 1
        self._is_occupied = False

    @property
    def room_number(self):
        return self._room_number

    @room_number.setter
    def room_number(self, new_n):
        self._room_number = new_n

    @property
    def room_type(self):
        return self._room_type

    @room_type.setter
    def room_type(self, new_rt):
        if new_rt in (self.RoomType.SINGLE, self.RoomType.DOUBLE, self.RoomType.ICU):
            self._room_type = new_rt
        else:
            raise ValueError(f"Invalid room type: {new_rt}. Room type must be one of: Single, Double, ICU.")

    @property
    def daily_rate(self):
        return self._daily_rate

    @daily_rate.setter
    def daily_rate(self, new_dr):
        if not isinstance(new_dr, (int, float)):
            raise TypeError('Invalid type for daily rate. Should be integer or float.')
        if new_dr < 1:
            raise ValueError('Daily rate cannot be less than $1.')
        self._daily_rate = float(new_dr)

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, new_c):
        if not isinstance(new_c, int):
            raise TypeError('Invalid type for capacity. Should be integer.')
        elif not 1 <= new_c <= 2:
            raise ValueError('Capacity is minimum 1 and maximum 2.')

    @property
    def is_occupied(self):
        return self._is_occupied

    @is_occupied.setter
    def is_occupied(self, new_v):
        if not isinstance(new_v, bool):
            raise TypeError('Invalid type for occupancy. Should be true or false.')
        self._is_occupied = new_v

    def __str__(self):
        return f'Room: {self._room_number} | Type: {self._room_type} | Occupied: {self._is_occupied}'


