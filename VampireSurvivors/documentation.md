# Random documentation for stuff

## Entity

An entity will have the minimal necesarry attributes. Most of the logic will be in components that are attatched to
entities.\n
init(type, list_of_components)

### Properties

```
EntityType: Enum[EntityType]
Components: list[Components]
+update(dt: float)
+clean_up()

```

## Entity types

Enum over the different types of entities

```
Player
CircleEnemy
```

## Components

All of the entities logic will be in components. This should make it such that we can swap out the logic we need.
Some components needs sub-components aswell. An example is HealthBarComponent need spritecomponent and positioncomponent
ComponentInterface

```
Components: list[Components]
+update(dt: float)
```

Different components:

1. HealthComponent
2. HealthBarComponent(owner_health_component: HealthComponent)
3. CollisionComponent

Todo:

1. PositionalComponent (Position: Vector2, move(Direction: Enum[Direction]))
    - Another constructor that takes a positionalcomponent and an offset, such that we follow entity with offset
2. SpriteComponent
