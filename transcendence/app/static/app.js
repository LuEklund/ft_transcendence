function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const postRequest = async (url, data) => {
	const csrftoken = getCookie('csrftoken');
	const config = {
		method: "POST",
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(data)
	}
	try {
		const response = await fetch(url, config);
		if (!response.ok) {
			const info = {
				succeded: false,
				message: "failed to add new user"
			}
			return info;
		} else {
			const data = await response.json();
			data.succeded = true;
			return data;
		}
	} catch (error) {
		console.log(error);
		return ({ "success":false, "message": "Something happened. try again", "status":400})
	}
}

const putRequest = async (url, data) => {
	const csrftoken = getCookie('csrftoken');
	const config = {
		method: "PUT",
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(data)
	}
	try {
		const response = await fetch(url, config);
		if (!response.ok) {
			const info = {
				succeded: false,
				message: "failed to add new user"
			}
			return info;
		} else {
			const data = await response.json();
			return data;
		}
	} catch (error) {
		console.log(error);
	}
}

const deleteRequest = async (url) => {
	const csrftoken = getCookie('csrftoken');
	const config = {
		method: "DELETE",
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
	}
	try {
		const response = await fetch(url, config);
		const json = await response.json();
		console.log(json);
		return json;
	} catch (error) {
		console.log(error);
	}
}

const showLoadingSpinner = () => {
	const loadingSpinner = document.getElementById("loadingSpinnerContainer");
	loadingSpinner.style.display = "flex";
}

const hideLoadingSpinner = () => {
	const loadingSpinner = document.getElementById("loadingSpinnerContainer");
	loadingSpinner.style.display = "none";
}

const navigateTo = async (url) => {
	history.pushState(null, null, url);
	await window.handleLocation();
}

const goBack = async () => {
	history.back();
	await handleLocation();
}
