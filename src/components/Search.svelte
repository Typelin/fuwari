<script lang="ts">
import Icon from "@iconify/svelte";
import { url } from "@utils/url-utils.ts";
import { onMount } from "svelte";

interface SearchResult {
	url: string;
	meta: {
		title: string;
	};
	excerpt: string;
	urlPath?: string;
}

let keywordDesktop = "";
let keywordMobile = "";
let result: SearchResult[] = [];
let isSearching = false;
let posts: any[] = [];

const togglePanel = () => {
	const panel = document.getElementById("search-panel");
	panel?.classList.toggle("float-panel-closed");
	if (panel && !panel.classList.contains("float-panel-closed")) {
		// phones/tablets: put the cursor straight into the panel's input
		setTimeout(() => document.querySelector<HTMLInputElement>("#search-bar-inside input")?.focus(), 50);
	}
};

const closePanel = () => {
	document.getElementById("search-panel")?.classList.add("float-panel-closed");
};

/** Arrow keys move between results, Escape closes the panel. */
const onSearchKey = (e: KeyboardEvent) => {
	const panel = document.getElementById("search-panel");
	if (!panel) return;
	if (e.key === "Escape") {
		closePanel();
		(document.activeElement as HTMLElement | null)?.blur();
		return;
	}
	if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
	const links = Array.from(panel.querySelectorAll<HTMLAnchorElement>("a.search-result"));
	if (!links.length) return;
	e.preventDefault();
	const i = links.indexOf(document.activeElement as HTMLAnchorElement);
	const next = e.key === "ArrowDown" ? (i < 0 ? 0 : Math.min(links.length - 1, i + 1)) : i - 1;
	if (next < 0) {
		const desktop = document.querySelector<HTMLInputElement>("#search-bar input");
		const input = desktop && getComputedStyle(desktop).display !== "none" ? desktop : document.querySelector<HTMLInputElement>("#search-bar-inside input");
		input?.focus();
	} else {
		links[next].focus();
	}
};

const escapeHtml = (t: string) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const escapeRegExp = (t: string) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

onMount(() => {
	const onKey = (e: KeyboardEvent) => {
		if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
			e.preventDefault();
			const desktop = document.querySelector<HTMLInputElement>('#search-bar input');
			if (desktop && getComputedStyle(desktop).display !== "none") {
				desktop.focus();
			} else {
				togglePanel();
			}
		}
	};
	window.addEventListener("keydown", onKey);
	// Escape anywhere closes an open search panel
	const onEsc = (e: KeyboardEvent) => {
		if (e.key === "Escape" && !document.getElementById("search-panel")?.classList.contains("float-panel-closed")) closePanel();
	};
	window.addEventListener("keydown", onEsc);
	return () => {
		window.removeEventListener("keydown", onKey);
		window.removeEventListener("keydown", onEsc);
	};
});

const setPanelVisibility = (show: boolean, isDesktop: boolean): void => {
	const panel = document.getElementById("search-panel");
	if (!panel || !isDesktop) return;

	if (show) {
		panel.classList.remove("float-panel-closed");
	} else {
		panel.classList.add("float-panel-closed");
	}
};

/** Escape the excerpt first (it is rendered as HTML), then mark the keyword. */
const highlightText = (text: string, keyword: string): string => {
	const safe = escapeHtml(text);
	if (!keyword) return safe;
	const regex = new RegExp(`(${escapeRegExp(escapeHtml(keyword))})`, "gi");
	return safe.replace(regex, "<mark>$1</mark>");
};

const search = async (keyword: string, isDesktop: boolean): Promise<void> => {
	if (!keyword) {
		setPanelVisibility(false, isDesktop);
		result = [];
		return;
	}

	isSearching = true;

	try {
		const searchResults = posts
			.filter((post) => {
				const keywordLower = keyword.toLowerCase();
				const searchText =
					`${post.title} ${post.description} ${post.content}`.toLowerCase();
				const urlPath = `/posts/${post.link}`;

				// 支援內容搜尋和 URL 字尾搜尋
				return (
					searchText.includes(keywordLower) ||
					urlPath.toLowerCase().includes(keywordLower) ||
					post.link.toLowerCase().includes(keywordLower)
				);
			})
			.map((post) => {
				const contentLower = post.content.toLowerCase();
				const keywordLower = keyword.toLowerCase();
				const contentIndex = contentLower.indexOf(keywordLower);

				let excerpt = "";
				if (contentIndex !== -1) {
					const start = Math.max(0, contentIndex - 50);
					const end = Math.min(post.content.length, contentIndex + 100);
					excerpt = post.content.substring(start, end);
					if (start > 0) excerpt = "..." + excerpt;
					if (end < post.content.length) excerpt = excerpt + "...";
				} else {
					excerpt = post.description || post.content.substring(0, 150) + "...";
				}

				return {
					url: url(`/posts/${post.link}/`),
					meta: {
						title: post.title,
					},
					excerpt: highlightText(excerpt, keyword),
					urlPath: `/posts/${post.link}`,
				};
			});

		result = searchResults;
		setPanelVisibility(true, isDesktop); // keep it open so "no results" is visible too
	} catch (error) {
		console.error("Search error:", error);
		result = [];
		setPanelVisibility(false, isDesktop);
	} finally {
		isSearching = false;
	}
};

onMount(async () => {
	try {
		const response = await fetch("/rss.xml");
		const text = await response.text();
		const parser = new DOMParser();
		const xml = parser.parseFromString(text, "text/xml");
		const items = xml.querySelectorAll("item");

		posts = Array.from(items).map((item) => {
			// 尝试多种方式获取content:encoded内容
			let content = "";
			const contentEncoded =
				item.getElementsByTagNameNS("*", "encoded")[0]?.textContent ||
				item.querySelector("*|encoded")?.textContent ||
				"";

			if (contentEncoded) {
				// decode the HTML, drop tags (including <br> written inside tables), collapse whitespace
				const doc = parser.parseFromString(contentEncoded, "text/html");
				content = (doc.body.textContent || "")
					.replace(/<\/?[a-z][^>]*>/gi, " ")
					.replace(/\s+/g, " ")
					.trim();
			}

			return {
				title: item.querySelector("title")?.textContent || "",
				description: item.querySelector("description")?.textContent || "",
				content: content,
				link:
					item
						.querySelector("link")
						?.textContent?.replace(/.*\/posts\/(.*?)\//, "$1") || "",
			};
		});
	} catch (error) {
		console.error("Error fetching RSS:", error);
	}
});

$: search(keywordDesktop, true);
$: search(keywordMobile, false);
</script>

<!-- search bar for desktop view -->
<div id="search-bar" class="relative hidden xl:flex transition-all items-center h-11 mr-2 rounded-lg
      bg-black/[0.04] hover:bg-black/[0.06] focus-within:bg-black/[0.06]
      dark:bg-white/5 dark:hover:bg-white/10 dark:focus-within:bg-white/10
">
    <Icon icon="material-symbols:search" class="absolute text-[1.25rem] pointer-events-none ml-3 transition my-auto text-black/30 dark:text-white/30"></Icon>
    <input placeholder="搜尋" aria-label="搜尋文章" bind:value={keywordDesktop} on:focus={() => search(keywordDesktop, true)} on:keydown={onSearchKey}
           class="transition-all pl-10 pr-12 text-sm bg-transparent outline-0
         h-full w-36 2xl:w-40 active:w-48 focus:w-48 2xl:active:w-56 2xl:focus:w-56 text-black/50 dark:text-white/50"
    >
    <kbd class="absolute right-3 pointer-events-none text-[0.7rem] font-mono px-1.5 py-0.5 rounded border border-black/15 dark:border-white/15 text-black/35 dark:text-white/35">⌘K</kbd></div>

<!-- toggle btn for phone/tablet view -->
<button on:click={togglePanel} aria-label="搜尋" id="search-switch"
        class="btn-plain scale-animation xl:!hidden rounded-lg w-11 h-11 active:scale-90">
    <Icon icon="material-symbols:search" class="text-[1.25rem]"></Icon>
</button>

<!-- search panel -->
<div id="search-panel" class="float-panel float-panel-closed search-panel absolute md:w-[30rem]
top-20 left-4 md:left-[unset] right-4 shadow-2xl rounded-2xl p-2">

    <!-- search bar inside panel for phone/tablet -->
    <div id="search-bar-inside" class="flex relative xl:hidden transition-all items-center h-11 rounded-xl
      bg-black/[0.04] hover:bg-black/[0.06] focus-within:bg-black/[0.06]
      dark:bg-white/5 dark:hover:bg-white/10 dark:focus-within:bg-white/10
  ">
        <Icon icon="material-symbols:search" class="absolute text-[1.25rem] pointer-events-none ml-3 transition my-auto text-black/30 dark:text-white/30"></Icon>
        <input placeholder="搜尋文章" aria-label="搜尋文章" type="search" enterkeyhint="search" bind:value={keywordMobile} on:keydown={onSearchKey}
               class="pl-10 absolute inset-0 text-sm bg-transparent outline-0
               focus:w-60 text-black/50 dark:text-white/50"
        >
    </div>

    <!-- search results -->
    {#each result as item}
        <a href={item.url} on:keydown={onSearchKey} on:click={closePanel}
           class="search-result transition first-of-type:mt-2 xl:first-of-type:mt-0 group block outline-none
       rounded-xl text-lg px-3 py-2 hover:bg-[var(--btn-plain-bg-hover)] focus-visible:bg-[var(--btn-plain-bg-hover)] active:bg-[var(--btn-plain-bg-active)]">
            <div class="transition text-90 inline-flex font-bold group-hover:text-[var(--primary)]">
                {item.meta.title}<Icon icon="fa6-solid:chevron-right" class="transition text-[0.75rem] translate-x-1 my-auto text-[var(--primary)]"></Icon>
            </div>
            <div class="transition text-xs text-30 mb-1 font-mono">
                {item.urlPath}
            </div>
            <div class="transition text-sm text-50">
                {@html item.excerpt}
            </div>
        </a>
    {/each}
    {#if (keywordDesktop || keywordMobile) && result.length === 0 && !isSearching}
        <p class="px-3 py-4 text-sm text-50">找不到符合「{keywordDesktop || keywordMobile}」的文章。</p>
    {/if}
</div>

<style>
  input:focus {
    outline: 0;
  }
  .search-panel {
    background-color: var(--float-panel-bg-opaque);
    max-height: calc(100vh - 100px);
    overflow-y: auto;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE and Edge */
  }

  .search-panel::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
</style>
