import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";

import Dashboard from "./pages/student/Dashboard";
import Rooms from "./pages/student/Rooms";
import MyRequests from "./pages/student/MyRequests";
import Notifications from "./pages/student/Notifications";
import BookRoom from "./pages/student/BookRoom";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Dashboard />}
                />

                <Route
                    path="/rooms"
                    element={<Rooms />}
                />
                
                <Route
                    path="/book-room/:roomId"
                    element={<BookRoom />}
                />
                <Route
                    path="/requests"
                    element={<MyRequests />}
                />

                <Route
                    path="/notifications"
                    element={<Notifications />}
                />

            </Routes>

        </BrowserRouter>

    );
}

export default App;