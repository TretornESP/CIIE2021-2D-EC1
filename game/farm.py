import pygame

class Farm(object):
    _object_pond   = pygame.sprite.Group()
    _enemy_pond    = pygame.sprite.Group()
    _platform_pond = pygame.sprite.Group()
    _trigger_pond  = pygame.sprite.Group()

    _dynamic_pond = pygame.sprite.Group()
    _static_pond  = pygame.sprite.Group()
    _overlay_pond = pygame.sprite.Group()

    _player = None

    @classmethod
    def push_to_close(cls):
        cls._object_pond.empty()
        cls._enemy_pond.empty()
        cls._platform_pond.empty()
        cls._trigger_pond.empty()

        cls._dynamic_pond.empty()
        cls._static_pond.empty()
        cls._overlay_pond.empty()

        _player = None

    @classmethod
    def draw_pond(cls, screen):
        cls._static_pond.draw(screen)
        cls._dynamic_pond.draw(screen)

    @classmethod
    def set_pond_position(cls, scr_x, v):
        for sprite in iter(cls._static_pond):
            sprite.set_position((scr_x, v))
        for sprite in iter(cls._dynamic_pond):
            sprite.set_position((scr_x, v))

    @classmethod
    def update_ponds(cls, elapsed_time):
        for enemy in cls._enemy_pond:
            enemy.move_cpu()
        cls._dynamic_pond.update(elapsed_time)
        cls._static_pond.update(elapsed_time)

    @classmethod
    def platform_collision(cls, target):
        platform = pygame.sprite.spritecollideany(target, cls._platform_pond)
        if platform != None and not platform.is_same(target):
            return platform
        return None

    @classmethod
    def enemy_collision(cls, target):
        enemy = pygame.sprite.spritecollideany(target, cls._enemy_pond)
        if enemy != None and not enemy.is_same(target):
            return enemy
        return None

    @classmethod
    def item_collision(cls, target):
        item = pygame.sprite.spritecollideany(target, cls._object_pond)
        if item != None and not item.is_same(target):
            return item
        return None

    @classmethod
    def trigger_collision(cls, target):
        trigger = pygame.sprite.spritecollideany(target, cls._trigger_pond)
        if trigger != None and not trigger.is_same(target):
            return trigger
        return None

    @classmethod
    def touches_anything_visible(cls, target):
        player = pygame.sprite.collide_rect(target, cls._player)
        item = pygame.sprite.spritecollideany(target, cls._object_pond)
        platform = pygame.sprite.spritecollideany(target, cls._platform_pond)

        return player or (item != None and not item.is_same(target)) or (platform != None and not platform.is_same(target))

    @classmethod
    def spawn_player(cls, player):
        cls._dynamic_pond.add(player)
        cls._player = player
        return cls._player

    @classmethod
    def add_enemy(cls, enemy):
        cls._enemy_pond.add(enemy)
        cls._dynamic_pond.add(enemy)

    @classmethod
    def add_platform(cls, platform):
        cls._platform_pond.add(platform)
        cls._static_pond.add(platform)

    @classmethod
    def add_object(cls, obj):
        cls._object_pond.add(obj)
        cls._static_pond.add(obj)

    @classmethod
    def add_trigger(cls, trigger):
        cls._trigger_pond.add(trigger)
        cls._static_pond.add(trigger)

    @classmethod
    def get_player(cls):
        if cls._player == None:
            raise SystemExit("Requested player before init")
        return cls._player

    @classmethod
    def free_killed_sprites(cls):
        print("Freeing unused memory")
        for sprite in cls._enemy_pond:
            if cls._dynamic_pond.has(sprite):
                continue
            cls._enemy_pond.remove(sprite)

        for sprite in cls._object_pond:
            if cls._static_pond.has(sprite):
                continue
            cls._object_pond.remove(sprite)

        for sprite in cls._trigger_pond:
            if cls._static_pond.has(sprite):
                continue
            cls._trigger_pond.remove(sprite)

        for sprite in cls._platform_pond:
            if cls._static_pond.has(sprite):
                continue
            cls._platform_pond.remove(sprite)
