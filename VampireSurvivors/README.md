# Vampire Survivors

## Todo
1. ~~Extract methods for getting angle and moving towards angle~~
2. ~~Extract method for two entities colliding~~
3. ~~Add Collision Detection (Move towards -angle for both entities if collision)~~ 
4. ~~Weapon System~~
5. ~~Sword Weapon~~
6. ~~Ensure that when fetching lists or modifying them that we only modify and return copies.~~ 
7. Pistol Weapon
8. ~~Show Health Bar~~
9. EXP system - Level up (RPG & EXP COMPONENTS)
10. Load pictures for entities
11. Cooldown for enemy attacks
12. ~~Components structure for reuse of code~~
13. Fps options
14. Fix amount of parameters on classes
15. Component for images that take radius
16. ~~Move diagioally is not 2x speed/1.5x~~
17. ~~Correctly cleanup entities~~
18. ~~Make keyinputs arrays, so multiple keys can do same input~~
19. Collision handler should ensure entities and collision objects are cleaned



## Refactors
1. CollisionObjects have component_id instead of owner_id and a description that says CollisionObjects only get created by collision components.
2. Components have method called get_owner_id(), which will be used for optimizing events, such that events have EventType, EntityId, callable



## Possible modifications
1. Optimized Collision Detection (preferably something not done before)
2. How to actually do events in a game
3. Move handler in components to a system