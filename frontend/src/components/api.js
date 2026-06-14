import { API } from "../config/env";

export async function apiFetch(url, options = {}) {
    let res = await fetch(url, {
        ...options,
        credentials: "include",
    });

    if (res.status === 401) {
        const refreshRes = await fetch(`${API.users}/refresh`, {
            method: "POST",
            credentials: "include",
        });

        if (!refreshRes.ok) {
            window.location.href = "/login";
            throw new Error("Session expired");
        }

        res = await fetch(url, {
            ...options,
            credentials: "include",
        });
    }

    return res;
}