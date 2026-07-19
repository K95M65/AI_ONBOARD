const REPOSITORY_URL = "https://github.com/K95M65/AI_ONBOARD";
const QUICKSTART = `git clone https://github.com/K95M65/AI_ONBOARD.git
python3 AI_ONBOARD/scripts/ai_onboard.py --global install \\
  --harness claude,codex,opencode --profile core --profile apple --agents`;

const routes = {
  website: {
    request: "“Build a clear, conversion-oriented project website.”",
    result: "A tested static site, independently reviewed and ready for an authorized publish.",
    stages: [
      { label: "Context", title: "Read the project contract", items: ["AGENTS.md", "brand evidence", "release boundary"] },
      { label: "Orchestrator", title: "Own the strategy-to-launch loop", items: ["design-and-build-website"] },
      { label: "Specialists", title: "Add only the expertise the route needs", items: ["define-brand-foundation", "design-product-content", "audit-accessibility"] },
      { label: "Independent lenses", title: "Challenge the implementation", items: ["design-review", "accessibility-review", "verifier"] },
      { label: "Evidence", title: "Prove the outcome in a real browser", items: ["test-browser-workflows", "responsive", "keyboard", "runtime"] },
    ],
  },
  product: {
    request: "“Turn an opportunity into a usable product interface.”",
    result: "A research-backed interaction model with coherent content, components, measurement, and release evidence.",
    stages: [
      { label: "Context", title: "Recover product intent and constraints", items: ["AGENTS.md", "existing system", "user evidence"] },
      { label: "Orchestrator", title: "Own the research-to-release loop", items: ["design-product-interface"] },
      { label: "Specialists", title: "Shape the product deliberately", items: ["shape-product-opportunity", "conduct-user-research", "design-product-content", "measure-product-experiments"] },
      { label: "Independent lenses", title: "Review quality outside the authoring context", items: ["design-review", "accessibility-review", "verifier"] },
      { label: "Evidence", title: "Validate workflows, states, and outcomes", items: ["task scenarios", "state coverage", "instrumentation"] },
    ],
  },
  apple: {
    request: "“Build or improve a native Apple-platform application.”",
    result: "An idiomatic Swift application with platform-appropriate UI, tested concurrency, persistence, accessibility, and performance.",
    stages: [
      { label: "Context", title: "Inspect targets, SDKs, and repository architecture", items: ["AGENTS.md", "Xcode project", "deployment targets"] },
      { label: "Orchestrator", title: "Own Apple implementation and review", items: ["develop-apple-platform-app"] },
      { label: "Specialists", title: "Load the relevant platform expertise", items: ["swift-architecture", "swift-concurrency", "swiftui-ui-patterns", "swiftdata-expert"] },
      { label: "Independent lenses", title: "Audit the native experience", items: ["design-review", "accessibility-review", "verifier"] },
      { label: "Evidence", title: "Build from current Apple guidance and exercise the target", items: ["official Apple source", "closest sample", "adaptation record", "Swift Testing"] },
    ],
  },
  security: {
    request: "“Map and reduce a system’s internal and external security exposure.”",
    result: "An owned attack-surface map, risk-ranked findings, evidence-tested controls, verified remediations, and a plan to detect change.",
    stages: [
      { label: "Context", title: "Establish authority, scope, and permitted actions", items: ["AGENTS.md", "scope", "rules of engagement"] },
      { label: "Orchestrator", title: "Own internal and external surface discovery", items: ["map-attack-surface"] },
      { label: "Specialists", title: "Assess paths, weaknesses, controls, and treatment", items: ["threat-model", "security-audit", "assess-security-controls", "manage-vulnerability-risk"] },
      { label: "Independent lenses", title: "Challenge evidence and risk decisions", items: ["security-review", "reviewer", "verifier"] },
      { label: "Evidence", title: "Prove coverage, correction, and change detection", items: ["asset ledger", "retest evidence", "monitoring plan"] },
    ],
  },
  cloudflare: {
    request: "“Build and ship a production Cloudflare workload.”",
    result: "A production-ready Worker or platform service with secure configuration, platform review, and deployment evidence.",
    stages: [
      { label: "Context", title: "Inspect bindings, runtime, and deployment state", items: ["AGENTS.md", "wrangler config", "Cloudflare resources"] },
      { label: "Orchestrator", title: "Own platform development and release", items: ["wrangler"] },
      { label: "Specialists", title: "Load service-specific guidance", items: ["workers-best-practices", "durable-objects", "agents-sdk", "cloudflare-one"] },
      { label: "Independent lenses", title: "Review runtime and security risk", items: ["security-review", "reviewer", "verifier"] },
      { label: "Evidence", title: "Exercise local and deployed behavior", items: ["wrangler checks", "smoke test", "observability"] },
    ],
  },
  analysis: {
    request: "“Understand a market and turn evidence into a decision.”",
    result: "A sourced analysis with explicit assumptions, structured reasoning, and a decision-ready narrative.",
    stages: [
      { label: "Context", title: "Frame the decision and evidence standard", items: ["decision owner", "scope", "source quality"] },
      { label: "Orchestrator", title: "Gather the market evidence", items: ["market-research"] },
      { label: "Specialists", title: "Structure and communicate the findings", items: ["competitive-intel", "analytical-frameworks", "data-storytelling", "dataviz"] },
      { label: "Independent lenses", title: "Test claims and interpretation", items: ["researcher", "reviewer", "verifier"] },
      { label: "Evidence", title: "Trace conclusions back to sources", items: ["citations", "assumptions", "decision criteria"] },
    ],
  },
  osint: {
    request: "“Investigate a public claim using lawful, open sources.”",
    result: "A reproducible evidence brief with resolved entities, confidence, contradictions, gaps, and privacy-aware reporting.",
    stages: [
      { label: "Context", title: "Define purpose, authority, and collection limits", items: ["public-source boundary", "legitimate purpose", "stopping condition"] },
      { label: "Orchestrator", title: "Own the evidence-led investigation", items: ["conduct-open-source-investigation"] },
      { label: "Specialists", title: "Preserve evidence and communicate only what fits", items: ["preserve-web-evidence", "data-storytelling", "dataviz"] },
      { label: "Independent lenses", title: "Challenge identity and inference", items: ["researcher", "reviewer", "verifier"] },
      { label: "Evidence", title: "Make every material claim reproducible", items: ["evidence ledger", "source provenance", "contradiction and gaps"] },
    ],
  },
  delivery: {
    request: "“Take a repository change from request through release.”",
    result: "A scoped, tested, reviewed change with an honest handoff and a traceable release path.",
    stages: [
      { label: "Manual opt-in · skipped by default", title: "Run GOAL or GRILL only when the user explicitly asks", items: ["grill-requirements", "goal-contract"] },
      { label: "Context", title: "Load repository rules and current evidence", items: ["AGENTS.md", "git diff", "retrieve-technical-docs"] },
      { label: "Build discipline", title: "Use only the workflow the change needs", items: ["develop-test-first", "debug-systematically", "simplify-code-safely"] },
      { label: "Specialists", title: "Apply task-specific delivery helpers", items: ["test-browser-workflows", "component-scaffold", "pr-description", "changelog"] },
      { label: "Independent lenses", title: "Review and verify before release", items: ["reviewer", "security-review", "verifier"] },
      { label: "Evidence", title: "Record what changed and what passed", items: ["tests", "diff review", "PR checks", "release notes"] },
    ],
  },
};

const state = {
  catalog: null,
  category: "All",
  query: "",
  expanded: false,
};

function routeMarkup(stage, index) {
  const chips = stage.items.map((item) => `<span>${item}</span>`).join("");
  return `
    <li>
      <span class="route-stage-index">${String(index + 1).padStart(2, "0")}</span>
      <div>
        <span class="route-label">${stage.label}</span>
        <h3>${stage.title}</h3>
        <div class="route-chips">${chips}</div>
      </div>
    </li>
  `;
}

function routeFromLocation() {
  const routeName = new URLSearchParams(window.location.search).get("route");
  return Object.prototype.hasOwnProperty.call(routes, routeName) ? routeName : "website";
}

function updateRouteHistory(routeName) {
  const url = new URL(window.location.href);
  const currentRoute = url.searchParams.get("route") || "website";
  if (currentRoute === routeName) return;
  if (routeName === "website") {
    url.searchParams.delete("route");
  } else {
    url.searchParams.set("route", routeName);
  }
  window.history.pushState({ route: routeName }, "", url);
}

function restoreCatalogStateFromLocation() {
  const url = new URL(window.location.href);
  const categories = ["All", ...state.catalog.categories.map(({ name }) => name)];
  const requestedCategory = url.searchParams.get("category") || "All";
  state.category = categories.includes(requestedCategory) ? requestedCategory : "All";
  state.query = url.searchParams.get("q") || "";
  state.expanded = false;
  document.querySelector("[data-skill-search]").value = state.query;
}

function updateCatalogHistory(push = false) {
  const url = new URL(window.location.href);
  if (state.category === "All") {
    url.searchParams.delete("category");
  } else {
    url.searchParams.set("category", state.category);
  }
  if (state.query.trim() === "") {
    url.searchParams.delete("q");
  } else {
    url.searchParams.set("q", state.query);
  }
  const method = push ? "pushState" : "replaceState";
  window.history[method](
    { route: routeFromLocation(), category: state.category, query: state.query },
    "",
    url,
  );
}

function renderRoute(routeName, announce = false) {
  const route = routes[routeName];
  document.querySelector("[data-route-request]").textContent = route.request;
  document.querySelector("[data-route-result]").textContent = route.result;
  document.querySelector("[data-route-stages]").innerHTML = route.stages
    .map(routeMarkup)
    .join("");

  document.querySelectorAll("[data-route]").forEach((button) => {
    const selected = button.dataset.route === routeName;
    button.classList.toggle("is-active", selected);
    button.setAttribute("aria-checked", String(selected));
    button.tabIndex = selected ? 0 : -1;
  });

  if (announce) {
    document.querySelector("[data-route-status]").textContent =
      `Route updated. ${route.request} End result: ${route.result}`;
  }
}

function updateCounts(counts) {
  Object.entries(counts).forEach(([name, value]) => {
    document.querySelectorAll(`[data-count="${name}"]`).forEach((node) => {
      node.textContent = value;
    });
  });
}

function renderCategoryFilters() {
  const container = document.querySelector("[data-category-filters]");
  const categories = ["All", ...state.catalog.categories.map(({ name }) => name)];
  container.replaceChildren(
    ...categories.map((category) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "category-filter";
      button.textContent = category;
      button.dataset.category = category;
      button.setAttribute("role", "radio");
      button.setAttribute("aria-checked", String(category === state.category));
      button.tabIndex = category === state.category ? 0 : -1;
      return button;
    }),
  );
}

function selectCategory(button, push = true) {
  state.category = button.dataset.category;
  document.querySelectorAll("[data-category]").forEach((candidate) => {
    const selected = candidate === button;
    candidate.setAttribute("aria-checked", String(selected));
    candidate.tabIndex = selected ? 0 : -1;
  });
  renderCatalog();
  updateCatalogHistory(push);
}

function matchingSkills() {
  const query = state.query.trim().toLocaleLowerCase();
  return state.catalog.skills.filter((skill) => {
    const matchesCategory = state.category === "All" || skill.category === state.category;
    const haystack = `${skill.name} ${skill.description} ${skill.category} ${skill.kind}`.toLocaleLowerCase();
    return matchesCategory && (!query || haystack.includes(query));
  });
}

function renderCatalog() {
  const list = document.querySelector("[data-skill-list]");
  const template = document.querySelector("#skill-row-template");
  const matches = matchingSkills();
  const hasFilters = state.category !== "All" || state.query.trim() !== "";
  const skills = state.expanded || hasFilters ? matches : matches.slice(0, 12);
  const fragment = document.createDocumentFragment();

  skills.forEach((skill, index) => {
    const row = template.content.cloneNode(true);
    row.querySelector(".skill-index").textContent = String(index + 1).padStart(2, "0");
    row.querySelector("h3").textContent = skill.name;
    row.querySelector(".skill-kind").textContent = `${skill.category} · ${skill.kind}`;
    row.querySelector("p").textContent = skill.description;
    const link = row.querySelector("a");
    link.href = `${REPOSITORY_URL}/blob/main/${skill.path}`;
    link.setAttribute("aria-label", `View ${skill.name} source on GitHub`);
    fragment.append(row);
  });

  if (skills.length === 0) {
    const empty = document.createElement("p");
    empty.className = "catalog-empty";
    empty.textContent = "No skills match this route. Clear the filters and try another term.";
    fragment.append(empty);
  }

  list.replaceChildren(fragment);
  document.querySelector("[data-catalog-count]").textContent =
    `${skills.length} of ${matches.length} matching skills shown`;
  document.querySelector("[data-clear-filter]").hidden =
    state.category === "All" && state.query === "";
  const showAll = document.querySelector("[data-show-all-skills]");
  showAll.hidden = hasFilters || matches.length <= 12;
  showAll.textContent = state.expanded
    ? "Show fewer skills"
    : `Show all ${matches.length} skills`;
}

function showToast(message) {
  const toast = document.querySelector("[data-toast]");
  toast.textContent = message;
  toast.hidden = false;
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    toast.hidden = true;
  }, 2400);
}

async function copyQuickstart() {
  const successMessage = "Install template copied — replace /path/to/project";
  try {
    await navigator.clipboard.writeText(QUICKSTART);
    showToast(successMessage);
  } catch {
    const textarea = document.createElement("textarea");
    textarea.value = QUICKSTART;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.append(textarea);
    textarea.select();
    const copied = document.execCommand("copy");
    textarea.remove();
    showToast(copied ? successMessage : "Copy failed — select the install template from the README");
  }
}

async function loadCatalog() {
  const response = await fetch("data/catalog.json");
  if (!response.ok) {
    throw new Error(`Catalog request failed: ${response.status}`);
  }
  state.catalog = await response.json();
  updateCounts(state.catalog.counts);
  restoreCatalogStateFromLocation();
  renderCategoryFilters();
  renderCatalog();
}

function setupInteractions() {
  const routeButtons = Array.from(document.querySelectorAll("[data-route]"));

  routeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      renderRoute(button.dataset.route, true);
      updateRouteHistory(button.dataset.route);
    });

    button.addEventListener("keydown", (event) => {
      const currentIndex = routeButtons.indexOf(button);
      const nextIndexByKey = {
        ArrowDown: (currentIndex + 1) % routeButtons.length,
        ArrowRight: (currentIndex + 1) % routeButtons.length,
        ArrowUp: (currentIndex - 1 + routeButtons.length) % routeButtons.length,
        ArrowLeft: (currentIndex - 1 + routeButtons.length) % routeButtons.length,
        Home: 0,
        End: routeButtons.length - 1,
      };
      const nextIndex = nextIndexByKey[event.key];
      if (nextIndex === undefined) return;

      event.preventDefault();
      const nextButton = routeButtons[nextIndex];
      nextButton.focus();
      renderRoute(nextButton.dataset.route, true);
      updateRouteHistory(nextButton.dataset.route);
    });
  });

  window.addEventListener("popstate", () => {
    renderRoute(routeFromLocation(), true);
    if (!state.catalog) return;
    restoreCatalogStateFromLocation();
    renderCategoryFilters();
    renderCatalog();
  });

  document.querySelector("[data-copy-command]").addEventListener("click", copyQuickstart);

  document.querySelector("[data-skill-search]").addEventListener("input", (event) => {
    state.query = event.target.value;
    renderCatalog();
    updateCatalogHistory();
  });

  const categoryFilters = document.querySelector("[data-category-filters]");
  categoryFilters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) return;
    selectCategory(button);
  });

  categoryFilters.addEventListener("keydown", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) return;
    const buttons = Array.from(categoryFilters.querySelectorAll("[data-category]"));
    const currentIndex = buttons.indexOf(button);
    const nextIndexByKey = {
      ArrowDown: (currentIndex + 1) % buttons.length,
      ArrowRight: (currentIndex + 1) % buttons.length,
      ArrowUp: (currentIndex - 1 + buttons.length) % buttons.length,
      ArrowLeft: (currentIndex - 1 + buttons.length) % buttons.length,
      Home: 0,
      End: buttons.length - 1,
    };
    const nextIndex = nextIndexByKey[event.key];
    if (nextIndex === undefined) return;

    event.preventDefault();
    const nextButton = buttons[nextIndex];
    nextButton.focus();
    selectCategory(nextButton);
  });

  document.querySelector("[data-clear-filter]").addEventListener("click", () => {
    document.querySelector("[data-skill-search]").focus();
    state.category = "All";
    state.query = "";
    state.expanded = false;
    document.querySelector("[data-skill-search]").value = "";
    renderCategoryFilters();
    renderCatalog();
    updateCatalogHistory();
  });

  document.querySelector("[data-show-all-skills]").addEventListener("click", () => {
    state.expanded = !state.expanded;
    renderCatalog();
  });

  const header = document.querySelector("[data-header]");
  const updateHeader = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
  window.addEventListener("scroll", updateHeader, { passive: true });
  updateHeader();
}

renderRoute(routeFromLocation());
setupInteractions();
loadCatalog().catch((error) => {
  console.error(error);
  document.querySelector("[data-catalog-count]").textContent =
    "The live catalog could not be loaded.";
  document.querySelector("[data-skill-search]").disabled = true;
  document.querySelector("[data-category-filters]").replaceChildren();
  document.querySelector("[data-clear-filter]").hidden = true;
  document.querySelector("[data-show-all-skills]").hidden = true;
  const fallback = document.createElement("a");
  fallback.className = "button";
  fallback.href = `${REPOSITORY_URL}/tree/main/skills`;
  fallback.textContent = "Browse skills on GitHub";
  document.querySelector("[data-skill-list]").replaceChildren(fallback);
});
