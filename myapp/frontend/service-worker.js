self.addEventListener("push", function (event) {

    const data = event.data.json();

    const title = data.title || "Notification";

    const options = {
        body: data.message || "You have a new notification.",
        icon: "/icon.png"
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});