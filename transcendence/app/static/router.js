window.route = (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, "", event.target.href);
    handleLocation();
};

const loaders = [
	{ path: "/", function: loadDashboard },
	{ path: "/signup", function: loadSignup },
	{ path: "/settings", function: loadSettings },
	{ path: "/pong", function: loadPong },
	{ path: "/pong/tournament", function: loadTournamentCreation },
	{ path: "/pong/tournament/*", function: loadTournamentLobby },
	{ path: "/pong/1v1", function: loadPong1v1 },
	{ path: "/users/*", function: loadUsersPage },
	{ path: "/pong/remoteTournament", function: loadRemoteTournamentPage },
]

const load = (path) => {
	const match = loaders.find(l => {
		if (l.path.includes("*")) {
			const basePath = l.path.replace("*", "");
			const pathSplit = path.split("/");
			const basePathSplit = basePath.split("/");
			if (path.startsWith(basePath) && pathSplit.length === basePathSplit.length)
				return true;
			else
				return false;
		} else {
			return l.path === path;
		}
	});
	if (match)
		match.function();
}

const parser = new DOMParser();
const handleLocation = async () => {
	const path = window.location.pathname;
	try {
		showLoadingSpinner();
		const response = await fetch(path);
		if (!response.ok) {
			window.history.pushState(null, null, "/");
			handleLocation();
			//throw new Error(`Failed to fetch route. Status: ${response.status}`);
		}
		const html = await response.text();
		if (document.body) {
			const doc = parser.parseFromString(html, 'text/html');
			const bodyContent = doc.body.innerHTML;
			document.body.innerHTML = bodyContent;
		}
		load(path);
		hideLoadingSpinner();
	} catch (error) {
		console.log(error);
		//Maybe we should send something to front end here!!!
	}
};

window.onpopstate = handleLocation;
handleLocation();

window.handleLocation = handleLocation;
