import {
	Command,
	CommandEmpty,
	type CommandEmptyProps,
	CommandGroup,
	CommandInput,
	type CommandInputProps,
	CommandItem,
	CommandList,
} from "@/components/ui/command";
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { Button, type ButtonProps } from "@/shared/components/Button";
import type { SelectableItem } from "@/shared/items";

import { Check, ChevronDown, ChevronUp } from "lucide-react";
import { useMemo, useState } from "react";

export interface MultiSelectComboboxProps<TItem> {
	buttonProps?: ButtonProps;
	commandInputProps?: Omit<CommandInputProps, "children">;
	commandEmptyProps?: CommandEmptyProps;
	onItemToggled?: (item: TItem) => void;
	onItemsUnselected?: (item: TItem[]) => void;
	items: readonly SelectableItem<TItem>[];
	getItemLabel: (item: SelectableItem<TItem>) => string;
	getItemValue: (item: SelectableItem<TItem>) => string;
}
type SelectableItemEnhanced<T> = SelectableItem<T> & {
	label: string;
	value: string;
};
export function MultiSelectCombobox<TITem>({
	items,
	onItemToggled,
	getItemLabel,
	getItemValue,
	buttonProps,
	commandInputProps,
	commandEmptyProps,
	onItemsUnselected,
}: MultiSelectComboboxProps<TITem>) {
	const [open, setOpen] = useState(false);
	const [value, setValue] = useState("");
	const enhancedItems = useMemo(
		() =>
			items.map(
				(item) =>
					({
						...item,
						label: getItemLabel(item),
						value: getItemValue(item),
					}) satisfies SelectableItemEnhanced<TITem>,
			),
		[items, getItemLabel, getItemValue],
	);
	const hasSelectedItems = useMemo(
		() => items.some((item) => item.isSelected),
		[items],
	);
	return (
		<Popover open={open} onOpenChange={setOpen}>
			<PopoverTrigger asChild>
				<Button {...buttonProps} aria-expanded={open}>
					{value
						? enhancedItems.find(({ label }) => label === value)?.label
						: buttonProps?.children}
					{!open ? <ChevronDown /> : <ChevronUp />}
				</Button>
			</PopoverTrigger>
			<PopoverContent>
				<>
					<Command>
						{commandInputProps && <CommandInput {...commandInputProps} />}
						<CommandList>
							{commandEmptyProps && <CommandEmpty {...commandEmptyProps} />}
							<CommandGroup>
								{enhancedItems.map(({ item, isSelected, value, label }) => (
									<CommandItem
										key={value}
										value={value}
										onSelect={(cutYear) => {
											onItemToggled?.(item);
											setValue(cutYear === value ? "" : cutYear);
											setOpen(false);
										}}
									>
										{label}
										<Check
											className={cn(
												"ml-auto",
												isSelected ? "opacity-100" : "opacity-0",
											)}
										/>
									</CommandItem>
								))}
							</CommandGroup>
						</CommandList>
					</Command>
					<Button
						disabled={!hasSelectedItems}
						variant={"destructive"}
						onClick={() => onItemsUnselected?.(items.map(({ item }) => item))}
					>
						Réinitialiser
					</Button>
				</>
			</PopoverContent>
		</Popover>
	);
}
