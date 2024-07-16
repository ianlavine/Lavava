import "../../styles/style.css";
import React, { useState } from "react";

type AbilityProps = {
    title: string;
    desc: string;
    extra: string;
    usage: string;
    onClick: () => void;
    onClose: () => void;
    isExpanded: boolean;
};

type AbilityData = {
    Name: string;
    Description: string;
    Extra_Description: string;
    Usage: string;
};

type DataStructure = {
    [key: string]: AbilityData[];
};

const data: DataStructure = {
    "1 Credit Abilities": [
        {
            Name: "Spawn",
            Description: "Claim an unclaimed node",
            Extra_Description: "Starting energy for a spawned node is 5",
            Usage: "Click on the node you want to spawn on."
        },
        {
            Name: "Freeze",
            Description: "Make a dynamic edge directional",
            Extra_Description: "It'll swap and freeze in your advantage",
            Usage: "Click on the dynamic edge you want to freeze."
        },
        {
            Name: "Burn",
            Description: "Convert a port node into a standard node",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the port node you want to burn."
        },
        {
            Name: "Zombie",
            Description: "Turn a node you own into a Zombie State, making it harder to capture.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want to turn into a Zombie State."
        }
    ],
    "2 Credit Abilities": [
        {
            Name: "Bridge",
            Description: "Create an edge between two port-nodes",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the first node you want to bridge, then click on the second node you want to bridge to."
        },
        {
            Name: "D-Bridge",
            Description: "Create a directional edge between two port-nodes",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the first node you want to D-Bridge, then click on the second node you want to D-Bridge to."
        },
        {
            Name: "Rage",
            Description: "Increase energy transfer rate from your nodes by 2.5 times.",
            Extra_Description: "Not sure what to put here",
            Usage: "Once clicked, all nodes you own will be enraged for the next 10 seconds."
        },
        {
            Name: "Poison",
            Description: "Send poison along edges, causing affected nodes to lose energy over 20 seconds.",
            Extra_Description: "Not sure what to put here",
            Usage: ""
        }
    ],
    "3 Credit Abilities": [
        {
            Name: "Nuke",
            Description: "Destroy all nodes in designated area surrounding the users capital node",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want to nuke from. It cannot have a structure built on it."
        },
        {
            Name: "Capital",
            Description: "Turn a full node into a capital, changing its energy dynamics and acting as a win condition.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want to turn into a capital. It cannot have a structure already built on it."
        },
        {
            Name: "Cannon",
            Description: "Fire a cannonball at an enemy node, dealing damage and reducing energy.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on one of your own nodes you want a cannon to be built on, then click on the enemy node you want to fire at."
        },
        {
            Name: "Pump",
            Description: "Place on a node to replenish abilities once fully charged.",
            Extra_Description: "Not sure what to put here",
            Usage: "Click on the node you want the pump to be placed on. It cannot have a structure already built on it."
        }
    ]
};

const Ability: React.FC<AbilityProps> = ({ title, desc, extra, usage, onClick, onClose, isExpanded }) => (
    <div className={`HtPability-window ${isExpanded ? "expanded" : ""}`} onClick={!isExpanded ? onClick : undefined}>
        {isExpanded && <button className="HtPclose-button" onClick={onClose}>×</button>}
        <h1>{title}</h1>
        <h2>{desc}</h2>
        {isExpanded && (
            <>
                <h3>{usage}</h3>
                <p>{extra}</p>
            </>
        )}
    </div>
);

const AbilitiesList: React.FC<{ data: DataStructure }> = ({ data }) => {
    const [expandedAbility, setExpandedAbility] = useState<string | null>(null);

    const handleAbilityClick = (abilityName: string) => {
        setExpandedAbility(abilityName === expandedAbility ? null : abilityName);
    };

    const handleClose = () => {
        setExpandedAbility(null);
    };

    return (
        <div className="HtPabilities-container">
            {Object.keys(data).map((category) =>
                data[category].map((ability, index) => {
                    const isExpanded = expandedAbility === ability.Name;
                    return (
                        <Ability
                            key={`${category}-${index}`}
                            title={ability.Name}
                            desc={ability.Description}
                            extra={ability.Extra_Description}
                            usage={ability.Usage}
                            onClick={() => handleAbilityClick(ability.Name)}
                            onClose={handleClose}
                            isExpanded={isExpanded}
                        />
                    );
                })
            )}
        </div>
    );
};

const HowToPlay: React.FC = () => {
    return (
        <div className="scrollable-container">
            <h1>How To Play</h1>
            <section className="space">
                <h2>Welcome to the game!</h2>
                <p>
                    This real-time strategy game is a thrilling twist on the classic board game Risk, built around the principles of graph theory. Here’s how to dive in and start playing:
                </p>
            </section>
            <section className="space">
                <h2>Game Overview</h2>
                <ul>
                    <li>
                        <strong>Nodes and Edges:</strong> Instead of countries, you'll control nodes, and instead of borders, nodes are connected by edges. These edges determine the flow of energy and attacks.
                    </li>
                    <li>
                        <strong>Energy Growth:</strong> Each node you own generates energy at a constant rate automatically. This energy is visually represented by the size of the nodes.
                    </li>
                    <li>
                        <strong>Real-Time Actions:</strong> Both attacking and reallocating energy occur in real time across the map.
                    </li>
                </ul>
            </section>
            <section className="space">
                <h2>Gameplay Mechanics</h2>
                <h3>1. Energy Growth</h3>
                <ul>
                    <li>Nodes you control will naturally grow in energy over time without any action needed from you.</li>
                    <li>The growth rate is constant and contributes to the node's size, indicating its energy level.</li>
                </ul>
                <h3>2. Attacking and Energy Transfer</h3>
                <ul>
                    <li><strong>Directional Edges:</strong> Each edge connecting nodes is directional and can be turned on or off by the owner of the "from-node".</li>
                    <li><strong>Energy Transfer Between Teammate Nodes:</strong> If an edge is turned on between two nodes you own (same color), energy will transfer in the direction the edge points.</li>
                    <li><strong>Attacking Opponent Nodes:</strong> If an edge is turned on between your node and an opponent's node, energy will be deducted equally from both nodes.</li>
                    <li><strong>Node Capture:</strong> If the attacked node’s energy drops to zero before the attacking node’s energy, the attacked node changes ownership to the attacker, adopting the attacker's color.</li>
                </ul>
                <p>Nodes continue to grow and transfer energy throughout the game until only one player remains with nodes of their color.</p>
            </section>
            <section className="space">
                <h2>Abilities</h2>
                <p>In addition to the basic gameplay mechanics, you can use abilities to gain an advantage over your opponents. Here are some of the abilities you can use:</p>
                <AbilitiesList data={data} />
            </section>
        </div>
    );
};

export default HowToPlay;
