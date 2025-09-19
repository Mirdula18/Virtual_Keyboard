class KeyboardLayouts:
    """Collection of different keyboard layouts"""
    
    QWERTY = {
        'name': 'QWERTY',
        'rows': [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ],
        'special_keys': ['SPACE', 'BACKSPACE', 'ENTER', 'SHIFT', 'CAPS']
    }
    
    DVORAK = {
        'name': 'DVORAK',
        'rows': [
            ["'", ',', '.', 'P', 'Y', 'F', 'G', 'C', 'R', 'L'],
            ['A', 'O', 'E', 'U', 'I', 'D', 'H', 'T', 'N', 'S'],
            [';', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z']
        ],
        'special_keys': ['SPACE', 'BACKSPACE', 'ENTER', 'SHIFT', 'CAPS']
    }
    
    NUMERIC = {
        'name': 'NUMERIC',
        'rows': [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['0', '.', '+']
        ],
        'special_keys': ['ENTER', 'BACKSPACE', 'CLEAR']
    }
    
    @staticmethod
    def get_layout(layout_name: str) -> dict:
        """Get a specific keyboard layout"""
        layouts = {
            'qwerty': KeyboardLayouts.QWERTY,
            'dvorak': KeyboardLayouts.DVORAK,
            'numeric': KeyboardLayouts.NUMERIC
        }
        
        return layouts.get(layout_name.lower(), KeyboardLayouts.QWERTY)
