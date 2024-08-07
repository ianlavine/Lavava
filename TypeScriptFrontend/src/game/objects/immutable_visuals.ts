export interface EventVisual {
    name: string;
    color: readonly [number, number, number]; 
}

export interface AbilityVisual {
    name: string;
    color: readonly [number, number, number]; 
    letter: string;
}

export function createEventVisual(name: string, color: readonly [number, number, number]): EventVisual {
    return Object({ name, color });
}

export function createAbilityVisual(name: string,  color: readonly [number, number, number] = [0, 0, 0], letter: string = ''): AbilityVisual {
    return Object({ name, color, letter });
}