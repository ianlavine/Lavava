import { IDItem } from "./idItem";
import { OtherPlayer } from "./otherPlayer";
import { MyPlayer } from "./myPlayer";
import {
    KeyCodes,
    MINIMUM_TRANSFER_VALUE,
    EventCodes,
    NUKE_OPTION_STRINGS,
    MINI_BRIDGE_RANGE,
} from "./constants";
import { ValidationFunction as ValidatorFunc, Point } from "./types";
import { Node } from "./node";
import { Edge } from "./edge";
import { ReloadAbility } from "./ReloadAbility";

function hasAnySame(
    num1: number,
    num2: number,
    num3: number,
    num4: number
): boolean {
    return num1 === num3 || num1 === num4 || num2 === num4 || num2 === num3;
}

function noClick(data: IDItem[]): boolean {
    return false;
}

function ownedBurnableNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.owner != null && burnableNode(data);
}

// Option for improved Burn, allowing preemptive burns before a node is owned
function burnableNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.is_port && node.edges.length != 0;
}

const standardNodeAttack = (data: IDItem, player: OtherPlayer): boolean => {
    const node = data as Node;
    return (
        node.owner !== player &&
        node.owner != null
    );
};

// Option for worse Nuke, requiring a node to be owned before attacking
const defaultNodeAttack = (data: IDItem, player: OtherPlayer): boolean => {
    const node = data as Node;
    return (
        node.stateName == "default" && standardNodeAttack(node, player)
    );
};

const isWithinScaledRange = (
    pos1: { x: number, y: number }, 
    pos2: { x: number, y: number }, 
    ratio: [number, number],
    range: number
): boolean => {
    const [ratioX, ratioY] = ratio;
    const scaledDx = (pos1.x - pos2.x) / ratioX;
    const scaledDy = (pos1.y - pos2.y) / ratioY;
    const scaledDistanceSquared = scaledDx ** 2 + scaledDy ** 2;
    return scaledDistanceSquared <= range ** 2;
};

// Option for improved Nuke, allowing attacks on unowned nodes (and theoretically one's own)
const defaultNode = (data: IDItem): boolean => {
    const node = data as Node;
    return node.stateName == "default";
}

const checkNewEdge = (nodeFrom: Node, nodeTo: Node, edges: Edge[]): boolean => {

    const newLine = new Phaser.Geom.Line(nodeFrom.pos.x, nodeFrom.pos.y, nodeTo.pos.x, nodeTo.pos.y);
    // Check for overlaps with all other edges
    for (let edge of edges) {
        if (!hasAnySame(nodeFrom.id, nodeTo.id, edge.from_node.id, edge.to_node.id) && Phaser.Geom.Intersects.LineToLine(newLine, edge.line)) {
            return false;
        }
    }
    return true;
};

function attackValidators(nodes: Node[], player: OtherPlayer, ratio: [number, number]) {
    return function structureRangedNodeAttack(data: IDItem[]): boolean {
        const node = data[0] as Node;
        const structures = nodes.filter(
            (node) =>  NUKE_OPTION_STRINGS.includes(node.stateName) && node.owner === player
        );

        const inStructureRange = (structure: Node): boolean => {
            const nukeRange = structure.state.nuke_range * structure.value;
            return isWithinScaledRange(node.pos, structue.pos, ratio, nukeRange);
        };

        return (
            defaultNode(node) &&
            structures.some((structure) => inStructureRange(structure))
        );
    };
}

function capitalValidator(getEdges: () => Edge[], player: OtherPlayer): ValidatorFunc {
    const neighbors = (node: Node): Node[] => {
        const neighbors: Node[] = [];
        getEdges().forEach((edge) => {
            try {
                const neighbor = edge.other(node);
                if (neighbor) neighbors.push(neighbor);
            } catch (error) {}
        });
        return neighbors;
    };

    return (data: IDItem[]): boolean => {
        const node = data[0] as Node; // Assuming data[0] is always a Node
        if (
            node.owner === player &&
            node.stateName == "default" &&
            node.full
        ) {
            let neighborCapital = false;
            for (const neighbor of neighbors(node)) {
                if (neighbor.stateName === "capital") {
                    neighborCapital = true;
                    break;
                }
            }
            return !neighborCapital;
        }
        return false;
    };
}

export function unownedNode(data: IDItem[]): boolean {
    const node = data[0] as Node;
    return node.owner === null && node.stateName === "default";
}

function playerValidators(player: OtherPlayer): {
    [key: string]: ValidatorFunc;
} {
    const myNode = (data: IDItem[]): boolean => {
        const node = data[0] as Node; // Type casting to Node for TypeScript
        return node.owner === player;
    };

    // Option for improved cannon, not requiring ports. Harder for bridge players to counter
    // Option for worsened Zombie, not allowing cannon/pump deletion before opponent takeover
    const myDefaultNode = (data: IDItem[]): boolean => {
        const node = data[0] as Node;
        return node.stateName === "default" && myNode(data);
    }

    const myDefaultPortNode = (data: IDItem[]): boolean => {
        const node = data[0] as Node;
        return node.is_port && myDefaultNode(data);
    }

    // Weakest Freeze.
    const dynamicEdgeOwnFromNode = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge; // Type casting to Edge for TypeScript
        return edge.dynamic && edge.from_node.owner === player;
    };

    // Middle Tier Freeze. If player is only the owner of to_node, then edge must not be flowing to swap
    const dynamicEdgeOwnEitherButNotFlowing = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge; // Type casting to Edge for TypeScript
        return edge.dynamic && (edge.from_node.owner === player || (edge.to_node.owner == player && !edge.flowing));
    };

    // Strongest Freeze. Can swap an incoming flowing edge, hard countering an attack
    const dynamicEdgeOwnEither = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge; // Type casting to Edge for TypeScript
        return edge.dynamic && (edge.from_node.owner === player || edge.to_node.owner == player);
    };

    const attackingEdge = (data: IDItem[]): boolean => {
        const edge = data[0] as Edge;
        return (
            edge.from_node.owner == player &&
            standardNodeAttack(edge.to_node, player)
        );
    };

    // Return an object mapping codes to their respective validator functions
    return {
        [KeyCodes.POISON_CODE]: attackingEdge,
        [KeyCodes.FREEZE_CODE]: dynamicEdgeOwnEitherButNotFlowing,
        [KeyCodes.ZOMBIE_CODE]: myDefaultNode,
        [KeyCodes.CANNON_CODE]: myDefaultPortNode,
        [KeyCodes.PUMP_CODE]: myDefaultNode,
    };
}

function newEdgeValidator(
    getEdges: () => Edge[],
    player: OtherPlayer,
    ratio: [number, number]
): { [key: string]: ValidatorFunc } {

    const newEdgeStandard = (data: Node[], ): boolean => {
        if (data.length === 1) {
            const firstNode = data[0];
            return firstNode.owner === player && firstNode.is_port;
        } else {
            const firstNode = data[0];
            const secondNode = data[1];
            return (
                firstNode.id !== secondNode.id &&
                secondNode.is_port &&
                checkNewEdge(firstNode, secondNode, getEdges())
            );
        }
    };

    const fullSizeEdgeValidator = (data: IDItem[]): boolean => {
        const nodes = data as Node[]; // Assert all data items are Nodes
        return (
            nodes.every((node) => node.portCount > 0) && newEdgeStandard(nodes)
        );
    };

    // Check if the nodes are within the range of a mini bridge
    const checkMiniBridgeRange = (nodes: Node[]): boolean => {
        if (nodes.length === 1) {
            return true;
        } else {
            const [node1, node2] = nodes;
            return isWithinScaledRange(node1.pos, node2.pos, ratio, MINI_BRIDGE_RANGE);
        }
    };
    
    const miniBridgeValidator = (data: IDItem[]): boolean => {
        const nodes = data as Node[];
        
        return (
            checkMiniBridgeRange(nodes) &&
            fullSizeEdgeValidator(nodes)
        );
    };

    return {
        [KeyCodes.BRIDGE_CODE]: fullSizeEdgeValidator,
        [KeyCodes.D_BRIDGE_CODE]: fullSizeEdgeValidator,
        [KeyCodes.MINI_BRIDGE_CODE]: miniBridgeValidator,
    };
}

export function makeAbilityValidators(
    player: MyPlayer,
    ratio: [number, number],
    nodes: Node[],
    getEdges: () => Edge[],
): { [key: string]: ValidatorFunc } {
    const abilityValidators: { [key: string]: ValidatorFunc } = {
        [KeyCodes.SPAWN_CODE]: unownedNode,
        [KeyCodes.BURN_CODE]: ownedBurnableNode,
        [KeyCodes.RAGE_CODE]: noClick,
        [KeyCodes.CAPITAL_CODE]: capitalValidator(getEdges, player),
        [KeyCodes.NUKE_CODE]: attackValidators(nodes, player, ratio),
    };

    // Merge the validators from `player_validators` into `abilityValidators`
    const playerValidatorsMap = playerValidators(player);
    const newEdgeValidators = newEdgeValidator(getEdges, player, ratio);
    return { ...abilityValidators, ...playerValidatorsMap, ...newEdgeValidators };
}

export function makeEventValidators(player: MyPlayer, getEdges: () => Edge[]): {
    [key: number]: (data: IDItem[]) => boolean;
} {
    function cannonShotValidator(data: IDItem[]): boolean {
        if (data.length === 1) {
            const firstNode = data[0] as Node;
            return (
                firstNode.owner === player &&
                firstNode.stateName === "cannon" &&
                firstNode.value > MINIMUM_TRANSFER_VALUE
            );
        } else if (data.length > 1) {
            const firstNode = data[0] as Node;
            const secondNode = data[1] as Node;
            return !(secondNode.owner === player && secondNode.full) &&
            checkNewEdge(firstNode, secondNode, getEdges());
        }
        return false;
    }

    function pumpDrainValidator(data: IDItem[]): boolean {
    const node = data[0] as Node;
        return (
            node.owner === player &&
            node.stateName === "pump" &&
            node.full
        );
    }

    function creditUsageValidator(data: IDItem[]): boolean {
        const ability = data[0] as ReloadAbility;
        return player.credits >= ability.credits;
    }

    function edgeValidator(data: IDItem[]): boolean {
        if (
            data instanceof Array &&
            data.length > 0 &&
            data[0] instanceof Edge
        ) {
            const edge = data[0] as Edge;
            return edge.controlledBy(player);
        }
        return false;
    }

    return {
        [EventCodes.CANNON_SHOT_CODE]: cannonShotValidator,
        [EventCodes.PUMP_DRAIN_CODE]: pumpDrainValidator,
        [EventCodes.STANDARD_LEFT_CLICK]: edgeValidator,
        [EventCodes.STANDARD_RIGHT_CLICK]: edgeValidator,
        [EventCodes.CREDIT_USAGE_CODE]: creditUsageValidator,
    };
}

