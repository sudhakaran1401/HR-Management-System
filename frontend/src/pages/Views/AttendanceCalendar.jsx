import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import PageHeader from "../../components/PageHeader";
import Loader from "../../components/Loader";

import { getAttendanceCalendarEvents } from "../../services/AttendanceService";

const AttendanceCalendar = () => {

    const navigate = useNavigate();

    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        const fetchCalendarEvents = async () => {

            try {

                const data = await getAttendanceCalendarEvents();
                setEvents(data);

            } catch (error) {

                console.error("Failed to load calendar events:", error);

            } finally {

                setLoading(false);

            }

        };

        fetchCalendarEvents();

    }, []);

    if (loading) {
        return <Loader />;
    }

    return (

    <div className="container mt-4">

        <PageHeader title="Attendance Calendar" />

        <div className="card shadow-sm border-0 calendar-card">

            <div className="card-body">

                <FullCalendar
                    plugins={[
                        dayGridPlugin,
                        interactionPlugin,
                    ]}
                    initialView="dayGridMonth"
                    height={650}
                    events={events}
                />

            </div>

        </div>

    </div>

    );
};

export default AttendanceCalendar;