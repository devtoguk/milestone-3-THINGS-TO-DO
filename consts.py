"""
Constants that will rarely change

Not held in a mongoDB collection to prevent extra database reads
just to populate a menu-dropdown or select field
"""
CATEGORIES = ('Animals', 'Attraction', 'Crafting',
              'Food', 'Nature', 'Sport and Leisure')

WHEN_TODO = ('Anytime', 'January', 'February', 'March', 'April', 'May',
             'June', 'July', 'August', 'September', 'October',
             'November', 'December')
