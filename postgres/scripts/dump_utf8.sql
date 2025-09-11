--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin;

--
-- Name: days; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.days (
    id integer NOT NULL,
    date date NOT NULL,
    work_hours integer NOT NULL,
    owner_id integer NOT NULL,
    CONSTRAINT check_work_hours_range CHECK (((0 <= work_hours) AND (work_hours <= 24)))
);


ALTER TABLE public.days OWNER TO admin;

--
-- Name: days_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.days_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.days_id_seq OWNER TO admin;

--
-- Name: days_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.days_id_seq OWNED BY public.days.id;


--
-- Name: failed_tasks; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.failed_tasks (
    id integer NOT NULL,
    owner_id integer NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.failed_tasks OWNER TO admin;

--
-- Name: failed_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.failed_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.failed_tasks_id_seq OWNER TO admin;

--
-- Name: failed_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.failed_tasks_id_seq OWNED BY public.failed_tasks.id;


--
-- Name: manual_days; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.manual_days (
    id integer NOT NULL,
    date date NOT NULL,
    work_hours integer NOT NULL,
    owner_id integer NOT NULL,
    CONSTRAINT check_work_hours_range CHECK (((0 <= work_hours) AND (work_hours <= 24)))
);


ALTER TABLE public.manual_days OWNER TO admin;

--
-- Name: manual_days_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.manual_days_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.manual_days_id_seq OWNER TO admin;

--
-- Name: manual_days_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.manual_days_id_seq OWNED BY public.manual_days.id;


--
-- Name: task_executions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.task_executions (
    id integer NOT NULL,
    task_id integer NOT NULL,
    day_id integer NOT NULL,
    owner_id integer NOT NULL,
    doing_hours integer NOT NULL
);


ALTER TABLE public.task_executions OWNER TO admin;

--
-- Name: task_executions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.task_executions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_executions_id_seq OWNER TO admin;

--
-- Name: task_executions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.task_executions_id_seq OWNED BY public.task_executions.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    deadline date,
    interest integer NOT NULL,
    importance integer NOT NULL,
    work_hours integer NOT NULL,
    owner_id integer NOT NULL,
    CONSTRAINT check_importance_range CHECK (((1 <= importance) AND (importance <= 10))),
    CONSTRAINT check_interest_range CHECK (((1 <= interest) AND (interest <= 10))),
    CONSTRAINT check_work_hours_range CHECK (((1 <= work_hours) AND (work_hours <= 24)))
);


ALTER TABLE public.tasks OWNER TO admin;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO admin;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    hashed_password character varying NOT NULL,
    is_active boolean NOT NULL,
    is_admin boolean NOT NULL
);


ALTER TABLE public.users OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: days id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.days ALTER COLUMN id SET DEFAULT nextval('public.days_id_seq'::regclass);


--
-- Name: failed_tasks id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.failed_tasks ALTER COLUMN id SET DEFAULT nextval('public.failed_tasks_id_seq'::regclass);


--
-- Name: manual_days id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.manual_days ALTER COLUMN id SET DEFAULT nextval('public.manual_days_id_seq'::regclass);


--
-- Name: task_executions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.task_executions ALTER COLUMN id SET DEFAULT nextval('public.task_executions_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alembic_version (version_num) FROM stdin;
da692a350960
\.


--
-- Data for Name: days; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.days (id, date, work_hours, owner_id) FROM stdin;
111	2025-01-01	0	1
112	2025-01-02	0	1
113	2025-01-03	2	1
114	2025-01-04	8	1
115	2025-01-05	4	1
116	2025-01-06	8	1
117	2025-01-07	4	1
118	2025-01-08	4	1
119	2025-01-09	4	1
120	2025-01-10	4	1
\.


--
-- Data for Name: failed_tasks; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.failed_tasks (id, owner_id, task_id) FROM stdin;
32	1	7
\.


--
-- Data for Name: manual_days; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.manual_days (id, date, work_hours, owner_id) FROM stdin;
1	2025-01-01	0	1
2	2025-01-02	0	1
3	2025-01-03	2	1
4	2025-01-04	8	1
5	2025-01-06	8	1
\.


--
-- Data for Name: task_executions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.task_executions (id, task_id, day_id, owner_id, doing_hours) FROM stdin;
51	6	113	1	2
52	8	114	1	2
53	5	114	1	6
54	1	115	1	2
55	5	115	1	2
56	2	116	1	6
57	3	116	1	2
58	4	118	1	2
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.tasks (id, name, deadline, interest, importance, work_hours, owner_id) FROM stdin;
1	╨Я╨╛╨┤╨│╨╛╤В╨╛╨▓╨╕╤В╤М╤Б╤П ╨║ ╨┐╨░╤А╨░╨╝	2025-01-06	3	8	2	1
2	╨Ф╨╛╨┐╨╕╤Б╨░╤В╤М ╤Б╨░╨╣╤В	\N	9	7	6	1
3	╨Ш╨╖╨╝╨╡╨╜╨╕╤В╤М ╤А╨╡╨╖╤О╨╝╨╡	\N	4	5	2	1
4	╨Я╨╛╨┤╨│╨╛╤В╨╛╨▓╨╕╤В╤М ╨┤╨╛╨╝╨░╤И╨╜╨╡╨╡ ╨╖╨░╨┤╨░╨╜╨╕╨╡	2025-01-09	4	9	2	1
5	╨Ш╨╖╤Г╤З╨╕╤В╤М ╨╜╨╛╨▓╤Г╤О ╤В╨╡╤Е╨╜╨╛╨╗╨╛╨│╨╕╤О	\N	10	6	8	1
6	╨Я╨╛╨╝╨╛╤З╤М ╨┤╤А╤Г╨│╤Г ╤Б ╨║╨╛╨╝╨┐╤М╤О╤В╨╡╤А╨╛╨╝	2025-01-04	3	5	2	1
7	╨Т╤Л╨┐╨╛╨╗╨╜╨╕╤В╤М ╨╖╨░╨┤╨░╨╜╨╕╨╡ ╨▓ ╨╕╨│╤А╨╡	2025-01-04	9	2	1	1
8	╨г╨▒╤А╨░╤В╤М╤Б╤П ╨┤╨╛╨╝╨░	2025-01-05	1	6	2	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, name, hashed_password, is_active, is_admin) FROM stdin;
1	chpdd	$2b$12$MZRZiB8XzQfshwYrbVQaOewrW2SaUhLTtoA5YAx3iBw9amR9WeyNi	t	t
2	kukuruska	$2b$12$T6u6x8165yzBqQFMca5iJ.M1uMTDjG0Tsbs/o.TqLABHdqFpVY/xW	t	f
3	popik	$2b$12$4/tYMgz.LjReVPbRS6rL0OOJStA8pwfvFBaHpbZfvj/1fnNOmmcRK	t	f
\.


--
-- Name: days_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.days_id_seq', 120, true);


--
-- Name: failed_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.failed_tasks_id_seq', 32, true);


--
-- Name: manual_days_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.manual_days_id_seq', 5, true);


--
-- Name: task_executions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.task_executions_id_seq', 58, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.tasks_id_seq', 8, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: days days_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.days
    ADD CONSTRAINT days_pkey PRIMARY KEY (id);


--
-- Name: failed_tasks failed_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.failed_tasks
    ADD CONSTRAINT failed_tasks_pkey PRIMARY KEY (id);


--
-- Name: manual_days manual_days_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.manual_days
    ADD CONSTRAINT manual_days_pkey PRIMARY KEY (id);


--
-- Name: task_executions task_executions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.task_executions
    ADD CONSTRAINT task_executions_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: days unique_date_for_user_days; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.days
    ADD CONSTRAINT unique_date_for_user_days UNIQUE (date, owner_id);


--
-- Name: manual_days unique_date_for_user_manual_days; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.manual_days
    ADD CONSTRAINT unique_date_for_user_manual_days UNIQUE (date, owner_id);


--
-- Name: tasks unique_task_name_per_owner; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT unique_task_name_per_owner UNIQUE (name, owner_id);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_days_owner_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_days_owner_id ON public.days USING btree (owner_id);


--
-- Name: ix_failed_tasks_owner_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_failed_tasks_owner_id ON public.failed_tasks USING btree (owner_id);


--
-- Name: ix_failed_tasks_task_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_failed_tasks_task_id ON public.failed_tasks USING btree (task_id);


--
-- Name: ix_manual_days_owner_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_manual_days_owner_id ON public.manual_days USING btree (owner_id);


--
-- Name: ix_task_executions_owner_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_task_executions_owner_id ON public.task_executions USING btree (owner_id);


--
-- Name: ix_tasks_owner_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_tasks_owner_id ON public.tasks USING btree (owner_id);


--
-- Name: owner_id_task_id_index; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX owner_id_task_id_index ON public.failed_tasks USING btree (owner_id, task_id);


--
-- Name: days days_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.days
    ADD CONSTRAINT days_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: failed_tasks failed_tasks_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.failed_tasks
    ADD CONSTRAINT failed_tasks_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: failed_tasks failed_tasks_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.failed_tasks
    ADD CONSTRAINT failed_tasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- Name: manual_days manual_days_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.manual_days
    ADD CONSTRAINT manual_days_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: task_executions task_executions_day_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.task_executions
    ADD CONSTRAINT task_executions_day_id_fkey FOREIGN KEY (day_id) REFERENCES public.days(id) ON DELETE CASCADE;


--
-- Name: task_executions task_executions_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.task_executions
    ADD CONSTRAINT task_executions_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: task_executions task_executions_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.task_executions
    ADD CONSTRAINT task_executions_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- Name: tasks tasks_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

