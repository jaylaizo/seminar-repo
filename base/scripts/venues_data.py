from base.models import Venue


def run():
    for venue_info in [
        ['DUCE/LRA/001', 120],
        ['DUCE/LRB/011', 120],
        ['DUCE/LRC/014', 120],
        ['DUCE/MTR',  80],
        ['LECT//HALL', 200],
        ['LECT/ROOM/119',120],
        ['LECT/ROOM/123',  120,],
        ['N/L/TH/A',  200 ],
        ['N/L/TH/B',  200],
        ['N/L/TH/C',200],
        ['LECT/HALL', 200],
        ['L/HALL', 200],
        ['LECTURE/ROOM/123',120],
        ['LECTURE/ROOM/119', 120],
        ]:

        venue = {
            'venue_name' : venue_info[0],
            'venue_capacity' : venue_info[1],
        }

        if not Venue.objects.filter(venue_name=venue_info[0]).exists():
            instance, created = Venue.objects.get_or_create(**venue)
