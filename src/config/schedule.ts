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
];

export const WEEKDAYS = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"] as const;

// schedule[dayIndex][slotIndex] — dayIndex: 0=Mon..6=Sun, slotIndex: 0=period1..8=period9
// null = no class
export const SCHEDULE: (ScheduleEntry | null)[][] = [
	// 週一
	[null, null, null, null, null, null, null, null, null],
	// 週二
	[
		{ name: "導師時間", location: "J206" },
		{ name: "電路板佈線實務", location: "J405" },
		{ name: "電路板佈線實務", location: "J405" },
		{ name: "電路板佈線實務", location: "J405" },
		null, null, null, null, null,
	],
	// 週三
	[
		null,
		{ name: "人工智慧實務", location: "B503" },
		{ name: "人工智慧實務", location: "B503" },
		{ name: "人工智慧實務", location: "B503" },
		{ name: "工程倫理與社會", location: "I0701" },
		{ name: "工程倫理與社會", location: "I0701" },
		null, null, null,
	],
	// 週四
	[
		null,
		{ name: "動態網頁設計", location: "J401" },
		{ name: "動態網頁設計", location: "J401" },
		{ name: "動態網頁設計", location: "J401" },
		{ name: "機率與統計", location: "J206" },
		{ name: "機率與統計", location: "J206" },
		{ name: "機率與統計", location: "J206" },
		null, null,
	],
	// 週五
	[
		null,
		{ name: "智慧健康產品設計", location: "X201" },
		{ name: "智慧健康產品設計", location: "X201" },
		{ name: "智慧健康產品設計", location: "X201" },
		null, null,
		{ name: "日本流行產業(B)", location: "W0502" },
		{ name: "日本流行產業(B)", location: "W0502" },
		{ name: "日本流行產業(B)", location: "W0502" },
	],
	// 週六
	[null, null, null, null, null, null, null, null, null],
	// 週日
	[null, null, null, null, null, null, null, null, null],
];
