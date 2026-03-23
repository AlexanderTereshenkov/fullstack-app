import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Alert,
  CircularProgress,
  Box,
} from '@mui/material';
import api from '../api';

export default function EventDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const user = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const res = await api.get(`/tickets/${id}`);
        setEvent(res.data);
        setFormData(res.data);
      } catch (err) {
        setError('Не удалось загрузить событие');
      } finally {
        setLoading(false);
      }
    };
    fetchEvent();
  }, [id]);

  const handleBuy = async () => {
    try {
      await api.post(`/user/add_ticket/${id}`);
      alert('Билет куплен!');
    } catch (err) {
      alert('Ошибка при покупке');
    }
  };

  const handleEdit = () => setEditing(true);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    try {
      await api.put(`/admin/update_ticket/${id}`, formData);
      setEvent(formData);
      setEditing(false);
      alert('Событие обновлено');
    } catch (err) {
      alert('Ошибка обновления');
    }
  };

  if (loading) return <CircularProgress sx={{ display: 'block', mx: 'auto', mt: 4 }} />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!event) return <Typography>Событие не найдено</Typography>;

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Card>
        <CardContent>
          {editing ? (
            <>
              <TextField
                fullWidth
                label="Название"
                name="title"
                value={formData.title}
                onChange={handleChange}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Дата"
                name="date"
                value={formData.date}
                onChange={handleChange}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Время"
                name="time"
                value={formData.time}
                onChange={handleChange}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Место"
                name="location"
                value={formData.location}
                onChange={handleChange}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Описание"
                name="description"
                value={formData.description}
                onChange={handleChange}
                multiline
                rows={4}
                margin="normal"
              />
              <Box sx={{ mt: 2 }}>
                <Button variant="contained" onClick={handleUpdate}>
                  Сохранить
                </Button>
                <Button variant="outlined" onClick={() => setEditing(false)} sx={{ ml: 1 }}>
                  Отмена
                </Button>
              </Box>
            </>
          ) : (
            <>
              <Typography variant="h4">{event.title}</Typography>
              <Typography color="textSecondary" gutterBottom>
                {event.date} {event.time}
              </Typography>
              <Typography variant="body1" paragraph>
                Место: {event.location}
              </Typography>
              <Typography variant="body2" paragraph>
                {event.description}
              </Typography>

              {user ? (
                user.role === 'admin' ? (
                  <Button variant="contained" onClick={handleEdit}>
                    Редактировать
                  </Button>
                ) : (
                  <Button variant="contained" onClick={handleBuy}>
                    Купить билет
                  </Button>
                )
              ) : (
                <Typography>Войдите, чтобы купить билет</Typography>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </Container>
  );
}