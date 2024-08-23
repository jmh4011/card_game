아 뭐 적지
```
card_game
├─ .gitignore
├─ alembic
│  ├─ env.py
│  ├─ README
│  ├─ script.py.mako
│  └─ versions
├─ alembic.ini
├─ Backup
│  ├─ db_backup_20240629.sql
│  ├─ db_backup_20240706.sql
│  ├─ db_backup_20240718.sql
│  ├─ db_backup_20240802.sql
│  └─ db_backup_20240809.sql
├─ client
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
│  │  ├─ favicon.ico
│  │  ├─ index.html
│  │  ├─ manifest.json
│  │  └─ robots.txt
│  ├─ src
│  │  ├─ api
│  │  │  ├─ api.ts
│  │  │  ├─ cards.ts
│  │  │  ├─ decks.ts
│  │  │  ├─ game.ts
│  │  │  ├─ static.ts
│  │  │  ├─ users.ts
│  │  │  └─ websocket.ts
│  │  ├─ App.css
│  │  ├─ App.tsx
│  │  ├─ assets
│  │  │  ├─ base_sprites.png
│  │  │  ├─ card-base
│  │  │  │  ├─ attack.png
│  │  │  │  ├─ character-frame.png
│  │  │  │  ├─ class.png
│  │  │  │  ├─ cost.png
│  │  │  │  ├─ description.png
│  │  │  │  ├─ frame.png
│  │  │  │  ├─ health.png
│  │  │  │  └─ name.png
│  │  │  └─ icon
│  │  │     └─ filter.png
│  │  ├─ atoms
│  │  │  ├─ global.ts
│  │  │  └─ modalConfigDeck.ts
│  │  ├─ components
│  │  │  ├─ Card.tsx
│  │  │  ├─ ModalSelectDeck.tsx
│  │  │  └─ ResponsiveText.tsx
│  │  ├─ custom.d.ts
│  │  ├─ index.css
│  │  ├─ index.tsx
│  │  ├─ pages
│  │  │  ├─ deck
│  │  │  │  ├─ components
│  │  │  │  │  ├─ CardInfo.tsx
│  │  │  │  │  ├─ SearchCards.tsx
│  │  │  │  │  ├─ SearchSetting.tsx
│  │  │  │  │  └─ ShowDeck.tsx
│  │  │  │  ├─ ConfigDeckPage.tsx
│  │  │  │  └─ SelectDeckPage.tsx
│  │  │  ├─ home
│  │  │  │  └─ HomePage.tsx
│  │  │  ├─ login
│  │  │  │  ├─ LoginPage.tsx
│  │  │  │  └─ SignUp.tsx
│  │  │  ├─ option
│  │  │  │  └─ OptionPage.tsx
│  │  │  ├─ play
│  │  │  │  ├─ components
│  │  │  │  │  └─ SelectMod.tsx
│  │  │  │  ├─ PlayPage.tsx
│  │  │  │  └─ TestPlay.tsx
│  │  │  └─ start
│  │  │     └─ StartPage.tsx
│  │  ├─ react-app-env.d.ts
│  │  ├─ setupTests.ts
│  │  └─ utils
│  │     ├─ styles.ts
│  │     ├─ types.ts
│  │     └─ Utiles.tsx
│  └─ tsconfig.json
├─ README.md
└─ server
   ├─ auth.py
   ├─ crud
   │  ├─ card.py
   │  ├─ deck.py
   │  ├─ deck_card.py
   │  ├─ game_history.py
   │  ├─ game_history_move.py
   │  ├─ game_mode.py
   │  ├─ user.py
   │  ├─ user_card.py
   │  ├─ user_deck_selection.py
   │  ├─ user_stats.py
   │  └─ __init__.py
   ├─ database.py
   ├─ main.py
   ├─ models.py
   ├─ modules
   │  ├─ cards
   │  │  └─ card.py
   │  ├─ game_manager.py
   │  ├─ player.py
   │  ├─ room_manager.py
   │  └─ __init__.py
   ├─ requirements.txt
   ├─ routers
   │  ├─ cards.py
   │  ├─ decks.py
   │  ├─ games.py
   │  └─ users.py
   ├─ schemas
   │  ├─ cards.py
   │  ├─ decks.py
   │  ├─ deck_cards.py
   │  ├─ game_historys.py
   │  ├─ game_historys_moves.py
   │  ├─ game_modes.py
   │  ├─ routers.py
   │  ├─ users.py
   │  ├─ user_cards.py
   │  ├─ user_deck_selections.py
   │  └─ user_stats.py
   ├─ services
   │  ├─ cards.py
   │  ├─ decks.py
   │  ├─ games.py
   │  ├─ users.py
   │  └─ __init__.py
   ├─ static
   │  └─ images
   │     ├─ backgraund
   │     │  ├─ 0.png
   │     │  └─ 1.png
   │     ├─ character
   │     │  ├─ 0.png
   │     │  ├─ 1.png
   │     │  ├─ 2.png
   │     │  └─ 3.png
   │     └─ field.png
   ├─ utils.py
   └─ __init__.py

```