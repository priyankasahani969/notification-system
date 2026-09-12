self.addEventListener("push", (event) => {
    console.log("Push event received");

    let data = {};

    try {
        data = event.data ? event.data.json() : {};
    } catch (error) {
        console.log("Push data is not JSON");

        data = {
            title: "Test Notification",
            body: event.data
                ? event.data.text()
                : "New notification"
        };
    }

    const title = data.title || "Notification";

    const options = {
        body: data.body || "You have a new notification."
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});


// Notification click

self.addEventListener("notificationclick", function (event) {

    event.notification.close();

    event.waitUntil(
        clients.matchAll({
            type: "window",
            includeUncontrolled: true
        }).then(function (clientList) {

            for (const client of clientList) {
                if ("focus" in client) {
                    return client.focus();
                }
            }

            if (clients.openWindow) {
                return clients.openWindow("/");
            }
        })
    );
});