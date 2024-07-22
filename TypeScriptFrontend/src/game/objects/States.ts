import { CANNON_NUKE_RANGE, CAPITAL_NUKE_RANGE, Colors, MineVisuals, PUMP_NUKE_RANGE } from "./constants";
import { random_equal_distributed_angles } from "./utilities"; // Ensure you import the angles function
import * as Phaser from "phaser";

export class State {
    name: string;
    graphic_override: boolean;
    nuke_range: number = 0;

    constructor(name: string, nuke_range = 0, gaphic_override: boolean = false) {
        this.name = name;
        this.nuke_range = nuke_range;
        this.graphic_override = gaphic_override;
    }

    select(on: boolean) {
        
    }

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        // Draw the state
    }

    removeSprites() {

    }
}

export class ZombieState extends State {
    zombieSprite: Phaser.GameObjects.Image | null = null;

    constructor(name: string) {
        super(name, 0, true);
    }

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        if (!this.zombieSprite) {
            this.zombieSprite = scene.add.image(pos.x, pos.y, "blackSquare");
            this.zombieSprite.setOrigin(0.5, 0.5); // Set origin to center for proper scaling
        }
        let currentScale = size / 20; // displayWidth considers current scale
        if (Math.abs(this.zombieSprite.scaleX - currentScale) > 0.01) {
            // threshold to avoid minor changes
            this.zombieSprite.setScale(currentScale);
        }
    }

    removeSprites() {
        this.zombieSprite?.destroy()
    }
}

export class MineState extends State {
    bubble: number;
    ringColor: readonly [number, number, number];
    unfilledColor: readonly [number, number, number];

    constructor(
        name: string,
        bubble: number,
        ringColor: readonly [number, number, number],
        unfilledColor: readonly [number, number, number] = Colors.GREY
    ) {
        super(name);
        this.bubble = bubble;
        this.ringColor = ringColor;
        this.unfilledColor = unfilledColor;
    }
 }

export class CapitalState extends State {
    capitalized: boolean;
    private starSprite: Phaser.GameObjects.Image | null = null;

    constructor(name: string, capitalized: boolean = false) {
        super(name, CAPITAL_NUKE_RANGE);
        this.capitalized = capitalized;
    }

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        if (this.capitalized) {
            if (!this.starSprite) {
                this.starSprite = scene.add.image(pos.x, pos.y, "star");
                this.starSprite.setOrigin(0.5, 0.5); // Set origin to center for proper scaling
            }
            let currentScale = size / 12; // displayWidth considers current scale
            if (Math.abs(this.starSprite.scaleX - currentScale) > 0.01) {
                // threshold to avoid minor changes
                this.starSprite.setScale(currentScale);
            }
        } else if (this.starSprite) {
            this.starSprite.destroy();
            this.starSprite = null;
        }
    }

    removeSprites() {
        this.starSprite?.destroy()
    }
}

export class CannonState extends State {
    angle: number;
    selected: boolean;

    constructor(
        name: string,
        angle: number = random_equal_distributed_angles(1)[0]
    ) {
        super(name, CANNON_NUKE_RANGE);
        this.angle = angle;
        this.selected = false;
    }

    select(on: boolean) {
        this.selected = on;
    }
}

export class PumpState extends State {
    private plusSprite: Phaser.GameObjects.Image | null = null;

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        if (!this.plusSprite) {
            this.plusSprite = scene.add.image(pos.x, pos.y, 'plus');
            this.plusSprite.setOrigin(0.5, 0.5); // Set origin to center for proper scaling
        }
        let currentScale = size / 12; // displayWidth considers current scale
        if (Math.abs(this.plusSprite.scaleX - currentScale) > 0.01) { // threshold to avoid minor changes
            this.plusSprite.setScale(currentScale);
        }
    }

    removeSprites() {
        this.plusSprite?.destroy();
    }

}

export const stateDict: { [key: number]: () => State } = {
    0: () => new State("default"),
    1: () => new ZombieState("zombie"),
    2: () => new CapitalState("capital", true),
    3: () =>
        new MineState("mine", MineVisuals.RESOURCE_BUBBLE, Colors.DARK_YELLOW),
    4: () =>
        new MineState(
            "mine",
            MineVisuals.ISLAND_RESOURCE_BUBBLE,
            Colors.YELLOW
        ),
    5: () => new CannonState("cannon"),
    6: () => new PumpState("pump", PUMP_NUKE_RANGE),
};

