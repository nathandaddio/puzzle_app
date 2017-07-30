def includeme(config):
    # config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('hitori_boards', r'/hitori_boards')
    config.add_route('hitori_board', r'/hitori_boards/{board_id:\d+}')
