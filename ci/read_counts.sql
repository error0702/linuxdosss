SELECT us.posts_read_count AS account,
       count(pt.post_number) FILTER (WHERE t.title = 'CI read receipt target') AS target,
       count(pt.post_number) FILTER (WHERE t.title = 'CI unread control topic') AS unread_control
FROM users u
JOIN user_stats us ON us.user_id = u.id
LEFT JOIN post_timings pt ON pt.user_id = u.id
LEFT JOIN topics t ON t.id = pt.topic_id
WHERE u.username = 'ci_reader'
GROUP BY us.posts_read_count;
