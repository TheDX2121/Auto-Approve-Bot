            # Build buttons from manual public channel URLs in 2x2 grid
            CHANNEL_URLS = [
                ("Channel 1", "https://t.me/yourchannel1"),
                ("Channel 2", "https://t.me/yourchannel2"),
                ("Channel 3", "https://t.me/yourchannel3"),
                ("Channel 4", "https://t.me/yourchannel4"),
            ]
            buttons = []
            for i in range(0, len(CHANNEL_URLS), 2):
                row = []
                for j in range(2):
                    if i + j < len(CHANNEL_URLS):
                        name, url = CHANNEL_URLS[i + j]
                        row.append(InlineKeyboardButton(f"✅ {name}", url=url))
                if row:
                    buttons.append(row)