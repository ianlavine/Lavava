import { State } from "./States";
import { Colors, GROWTH_STOP, PORT_COUNT } from "./constants";
import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "./enums";
import { phaserColor } from "./utilities";
import { CannonState } from "./States";
import { INode, IEdge } from "./graphTypeInterfaces";
import { random_equal_distributed_angles } from "./utilities";


export class Node extends IDItem implements INode {
    pos: Phaser.Math.Vector2;
    percents: [number, number];
    is_port: boolean;
    portPercent: number;
    ports: Array<number>;
    state: State;
    value: number;
    private _effects: Set<string>;
    private _owner: OtherPlayer | null;
    private _scene: Phaser.Scene;
    private graphics: Phaser.GameObjects.Graphics;
    private cannonGraphics: Phaser.GameObjects.Graphics;
    edges: IEdge[];

    constructor(
        id: number,
        pos: [number, number],
        is_port: boolean,
        state: State,
        value: number,
        _scene: Phaser.Scene
    ) {
        super(id, ClickType.NODE);
        this.percents = [pos[0] / 1000, pos[1] / 700];
        this.pos = new Phaser.Math.Vector2(pos[0], pos[1]);
        this.is_port = is_port;
        this.portPercent = 1;
        this.ports = this.is_port ? random_equal_distributed_angles(PORT_COUNT) : [];
        this.state = state;
        this.value = value;
        this.edges = [];
        this.effects = new Set();
        this.owner = null;
        this.scene = _scene;
        this.graphics = _scene.add.graphics();
        this.cannonGraphics = _scene.add.graphics();
    }

    public delete(): void {
        // Remove graphics from the scene
        if (this.graphics) {
            this.graphics.clear();
            this.graphics.destroy();
        }
    
        if (this.cannonGraphics) {
            this.cannonGraphics.clear();
            this.cannonGraphics.destroy();
        }
    }

    select(on: boolean): void {
            this.state.select(on);
    }

    get owner(): OtherPlayer | null {
        return this._owner;
    }

    set owner(owner: OtherPlayer | null) {
        this._owner = owner;
        this.influencedEdges.forEach((edge) => (edge.recolor = true));
    }

    get effects(): Set<string> {
        return this._effects;
    }

    set effects(effects: Set<string>) {
        this._effects = effects;
        this.outwardEdges.forEach((edge) => (edge.recolor = true));
    }

    get color(): readonly [number, number, number] {
        if (!this.owner) {
            return this.is_port ? Colors.BROWN : Colors.BLACK;
        }
        return this.owner.color;
    }

    get phaserColor(): number {
        return phaserColor(this.color);
    }

    get influencedEdges(): IEdge[] {
        return this.outwardEdges.filter((edge) => edge.on);
    }

    get outwardEdges(): IEdge[] {
        return this.edges.filter((edge) => edge.from_node === this);
    }

    get size(): number {
        return 5 + this.sizeFactor * 18;
    }
    get sizeFactor(): number {
        if (this.value < 5) return 0;
        return Math.max(
            Math.log10(this.value / 10) / 2 + this.value / 1000 + 0.15,
            0
        );
    }

    get stateName(): string {
        return this.state.name;
    }

    get full(): boolean {
        return this.value >= GROWTH_STOP;
    }

    get portCount(): number {
        return this.ports.length;
    }
    set scene(scene: Phaser.Scene) {
        this._scene = scene;
        this.resize();
        this.graphics = this._scene.add.graphics();
        this.cannonGraphics = this._scene.add.graphics();
    }
    burn(): boolean {
        this.portPercent -= 0.01;
        if (this.portPercent <= 0) {
            this.ports = [];
            return true;
        }
        return false;
    }

    draw(): void {
        this.graphics.clear();
        if (this.state.graphic_override) {
            this.state.draw(this._scene, this.size, this.pos);
            return;
        } else {
            if (this.effects.has("poison")) {
                this.graphics.lineStyle(6, phaserColor(Colors.PURPLE), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size + 4
                );
            }

            if (this.owner) {
                if (this.is_port) {
                    this.drawPorts(Colors.BROWN);
                } else if (this.ports.length > 0) {
                    this.drawPorts(Colors.ORANGE);
                    if (this.portPercent > 0) {
                        this.portPercent -= 0.05;
                    }
                    else {
                        this.ports = [];
                    }
                }
            }

            this.graphics.fillStyle(this.phaserColor, 1);
            this.graphics.fillCircle(this.pos.x, this.pos.y, this.size);

            if (this.effects.has("rage")) {
                this.graphics.lineStyle(3, phaserColor(Colors.DARK_GREEN), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size - 2
                );
            }
            if (this.full) {
                this.graphics.lineStyle(2, phaserColor(Colors.BLACK), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size + 1
                );
                if (this.stateName === "capital") {
                    this.graphics.lineStyle(2, phaserColor(Colors.PINK), 1);
                    this.graphics.strokeCircle(
                        this.pos.x,
                        this.pos.y,
                        this.size + 3
                    );
                }
            }

            this.state.draw(this._scene, this.size, this.pos);

            if (this.state instanceof CannonState) {
                this.cannonGraphics.clear();
                if (this.state.selected) {
                    let mousePos = this._scene.input.activePointer.position;
                    // Calculate angle between the spot and the mouse cursor
                    let dx = mousePos.x - this.pos.x;
                    let dy = mousePos.y - this.pos.y;
                    this.state.angle = Math.atan2(dy, dx) * (180 / Math.PI); // Angle in degrees
            
                    // Calculate distance to mouse cursor
                    let distanceToMouse = Math.sqrt(dx * dx + dy * dy) - this.size * 1.2;
            
                    // Draw the yellow rectangle from the cannon to the mouse cursor
                    this.drawRotatedRectangle(
                        this.state.angle,
                        distanceToMouse,  // Width is the distance to the mouse
                        this.size,        // Height remains the same as the cannon
                        Colors.LIGHT_YELLOW,  // Light yellow color
                        this.cannonGraphics,
                        0.8,  // Optional: a lesser alpha for lighter visibility
                        distanceToMouse / 2
                    );
                }

                this.drawRotatedRectangle(
                    this.state.angle,
                    this.size * 2,
                    this.size,
                    Colors.GREY,
                    this.cannonGraphics
                );
            }
        }
    }

    drawPorts(color: readonly [number, number, number]): void {
        const portWidth = this.size;
        const portHeight = this.size * 1.3;
        this.ports.forEach((angle) => {
            this.drawRotatedRectangle(angle, portWidth * this.portPercent, portHeight * this.portPercent, color);
        });
    }

    drawRotatedRectangle(
        angle: number,
        portWidth: number,
        portHeight: number,
        col: readonly [number, number, number],
        graphics: Phaser.GameObjects.Graphics = this.graphics,
        alpha: number = 1,  // Default opacity is 100%
        xOffset: number = 0  // Default to no offset
    ): void {
        const rad = Phaser.Math.DegToRad(angle);
        const halfWidth = portWidth / 2;
        const halfHeight = portHeight / 2;
        const distanceFromCenter = this.size * 1.2;
    
        const portCenter = new Phaser.Math.Vector2(
            this.pos.x + Math.cos(rad) * (distanceFromCenter + xOffset),
            this.pos.y + Math.sin(rad) * (distanceFromCenter + xOffset)
        );
    
        // Calculate the corners of the rotated rectangle
        const corners = [
            new Phaser.Math.Vector2(-halfWidth, -halfHeight),
            new Phaser.Math.Vector2(halfWidth, -halfHeight),
            new Phaser.Math.Vector2(halfWidth, halfHeight),
            new Phaser.Math.Vector2(-halfWidth, halfHeight),
        ].map(corner => corner.rotate(rad).add(portCenter));
    
        // Change graphics fill style here if needed
        graphics.fillStyle(
            Phaser.Display.Color.GetColor(col[0], col[1], col[2]),
            alpha
        );
    
        // Draw the polygon
        graphics.beginPath();
        graphics.moveTo(corners[0].x, corners[0].y);
        corners.forEach((corner, index) => {
            if (index > 0) graphics.lineTo(corner.x, corner.y);
        });
        graphics.closePath();
        graphics.fillPath();
    }

    resize(): void {
        // Adjust the position of the node based on newWidth and newHeight
        this.pos.x = this.percents[0] * Number(this._scene.game.config.width);
        this.pos.y = this.percents[1] * Number(this._scene.game.config.height);
        // Optionally, adjust the size or other properties here as needed
    }

}

