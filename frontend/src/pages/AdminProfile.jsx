import { useEffect, useState } from 'react';
import { Container, Typography, List, ListItem, ListItemText, IconButton, Button } from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function AdminProfile() {
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAdminEvents = async () => {
      const res = await api.get('/admin/me'); // предположим, что возвращает список событий админа
      setEvents(res.data.events);
    };
    fetchAdminEvents();
  }, []);

  const handleDelete = async (id) => {
    await api.delete(`/admin/delete_ticket/${id}`);
    setEvents(events.filter(e => e.id !== id));
  };

  const handleEdit = (id) => {
    navigate(`/admin/upload-poster?edit=${id}`); // можно переиспользовать форму загрузки для редактирования
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4">Мои события</Typography>
      <Button variant="contained" onClick={() => navigate('/admin/upload-poster')} sx={{ mb: 2 }}>
        Добавить событие
      </Button>
      <List>
        {events.map(event => (
          <ListItem key={event.id} divider secondaryAction={
            <>
              <IconButton edge="end" onClick={() => handleEdit(event.id)}>
                <Edit />
              </IconButton>
              <IconButton edge="end" onClick={() => handleDelete(event.id)}>
                <Delete />
              </IconButton>
            </>
          }>
            <ListItemText primary={event.title} secondary={event.date} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
}