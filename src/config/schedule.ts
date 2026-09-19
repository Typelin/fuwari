/**
 * Schedule data definition
 * Course names and locations only (no teacher names per requirement)
 */

export interface ScheduleEntry {
	name: string;
	location: string;
}

export interface TimeSlot {
	period: string;
	startTime: string;
	endTime: string;
}

export const TIME_SLOTS: TimeSlot[] = [
	{ period: "第1節", startTime: "08:10", endTime: "09:00" },
	{ period: "第2節", startTime: "09:10", endTime: "10:00" },
	{ period: "第3節", startTime: "10:10", endTime: "11:00" },
	{ period: "第4節", startTime: "11:10", endTime: "12:00" },
	{ period: "第5節", startTime: "12:50", endTime: "13:40" },
	{ period: "第6節", startTime: "13:50", endTime: "14:40" },
	{ period: "第7節", startTime: "14:50", endTime: "15:40" },
	{ period: "第8節", startTime: "15:50", endTime: "16:40" },
	{ period: "第9節", startTime: "16:50", endTime: "17:40" },
	{ period: "第11節", startTime: "18:20", endTime: "19:05" },
	{ period: "第12節", startTime: "19:05", endTime: "19:50" },
	{ period: "第13節", startTime: "20:00", endTime: "20:45" },
	{ period: "第14節", startTime: "20:45", endTime: "21:30" },
];

export const WEEKDAYS = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"] as const;

// schedule[dayIndex][slotIndex] — dayIndex: 0=Mon..6=Sun, slotIndex 對應 TIME_SLOTS
// null = no class
export const SCHEDULE: (ScheduleEntry | null)[][] = [
	// 週一
	[null, null, null, null, null, null, null, null, null, null, null, null, null],
	// 週二
	[null, null, null, null, null, null, null, null, null, null, null, null, null],
	// 週三
	[
		null, null, null,
		{ name: "導師時間", location: "J206" },
		null, null, null, null, null, null, null, null, null,
	],
	// 週四
	[
		{ name: "深度學習框架應用", location: "J201" },
		{ name: "深度學習框架應用", location: "J201" },
		{ name: "深度學習框架應用", location: "J201" },
		null, null, null, null, null, null, null, null, null, null,
	],
	// 週五
	[null, null, null, null, null, null, null, null, null, null, null, null, null],
	// 週六
	[null, null, null, null, null, null, null, null, null, null, null, null, null],
	// 週日
	[null, null, null, null, null, null, null, null, null, null, null, null, null],
];