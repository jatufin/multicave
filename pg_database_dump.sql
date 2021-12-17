--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5
-- Dumped by pg_dump version 12.5

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
-- Name: banned_words; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.banned_words (
    word character varying(30) NOT NULL
);


--
-- Name: condition_rooms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.condition_rooms (
    condition_id integer NOT NULL,
    game_id integer NOT NULL,
    room_tag character varying(10) NOT NULL
);


--
-- Name: conditions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conditions (
    id integer NOT NULL,
    game_id integer NOT NULL,
    room_tag character varying(10) NOT NULL,
    all_visited character varying(200) DEFAULT ''::character varying,
    not_all_visited character varying(200) DEFAULT ''::character varying,
    all_visited_choice character varying(50) DEFAULT ''::character varying,
    all_visited_target character varying(10) DEFAULT ''::character varying
);


--
-- Name: conditions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.conditions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: conditions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.conditions_id_seq OWNED BY public.conditions.id;


--
-- Name: current_rooms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.current_rooms (
    game_id integer NOT NULL,
    room_tag character varying(10) NOT NULL,
    player_id integer NOT NULL
);


--
-- Name: games; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.games (
    id integer NOT NULL,
    owner_id integer NOT NULL,
    published boolean DEFAULT false NOT NULL,
    title character varying(40) DEFAULT 'New game'::character varying NOT NULL,
    description character varying(256) DEFAULT ''::character varying,
    start_room character varying(10) DEFAULT ''::character varying
);


--
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    user_id integer NOT NULL,
    posting_date date DEFAULT CURRENT_DATE NOT NULL,
    body character varying(1024) NOT NULL
);


--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rooms (
    game_id integer NOT NULL,
    tag character varying(10) NOT NULL,
    title character varying(30) DEFAULT 'New room'::character varying NOT NULL,
    description character varying(1000) DEFAULT ''::character varying,
    first_visit_description character varying(1000) DEFAULT ''::character varying,
    next_visits_description character varying(1000) DEFAULT ''::character varying,
    endroom boolean DEFAULT false NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    locked boolean DEFAULT false NOT NULL,
    adm boolean DEFAULT false NOT NULL,
    username character varying(12) NOT NULL,
    password character varying(128) NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: visited_rooms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.visited_rooms (
    game_id integer NOT NULL,
    room_tag character varying(10) NOT NULL,
    player_id integer NOT NULL
);


--
-- Name: conditions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conditions ALTER COLUMN id SET DEFAULT nextval('public.conditions_id_seq'::regclass);


--
-- Name: games id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: banned_words; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.banned_words (word) FROM stdin;
\.


--
-- Data for Name: condition_rooms; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.condition_rooms (condition_id, game_id, room_tag) FROM stdin;
2	1	Room03
16	1	Room05
18	1	Room07
19	1	Room11
21	1	Room07
21	1	Room11
\.


--
-- Data for Name: conditions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.conditions (id, game_id, room_tag, all_visited, not_all_visited, all_visited_choice, all_visited_target) FROM stdin;
1	1	Room01	A hallway to the North goes deeper in the mountain.		Go North	Room02
2	1	Room02	A door to the West opens with the key you have.	To the West there is a locked door.	Go West.	Room04
3	1	Room02	There is an opening to East.		Go East	Room03
4	1	Room02	Hallway leads to the South.		Go South.	Room01
5	1	Room03	There is a corridor which leads back to the West.		Go West	Room02
6	1	Room04			Go East.	Room02
7	1	Room04			Go North	Room05
8	1	Room04			Go South	Room06
10	1	Room05			Go South	Room04
11	1	Room05			Descend the stairst to the North	Room07
13	1	Room06			Go North	Room04
14	1	Room06	The horrendous monster protects the entrance to the South.		Punch the Beast	Room09
16	1	Room06	Handy you have the nice sword.	Too bad you don't have a weapon.	Attack with the Sword	Room10
17	1	Room10	You can see glimmering red from a hole in the wall.		Crawl into the hole.	Room11
18	1	Room10	Great, you have that beautiful blue sapphire key!	You don't have the blue key!		
19	1	Room10	The smaragd key fits in the red lock.	You don't have the red key!		
20	1	Room11			Crawl back to the gate	Room10
21	1	Room10	You have keys to both of the locks!		Open the locks and open the gate.	Room12
22	1	Room10			Go Back to the Beast	Room06
12	1	Room07			Climb the stairway South	Room05
\.


--
-- Data for Name: current_rooms; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.current_rooms (game_id, room_tag, player_id) FROM stdin;
\.


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.games (id, owner_id, published, title, description, start_room) FROM stdin;
1	2	t	The Keys and the Beast	Thrilling adventure deep under the mountains.	Room01
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messages (id, user_id, posting_date, body) FROM stdin;
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rooms (game_id, tag, title, description, first_visit_description, next_visits_description, endroom) FROM stdin;
1	Room01	Entrance Hall	Only little sunshine is visible from outside.	You have entered the dungeon.	You are back where you started.	f
1	Room02	Dungeon room	A room in the dungeon. Stone walls are dark and unfriendly.	No more sunshine!	Same boring room.	f
1	Room03	Store room	This has been a store room full of all kinds of stuff.	You found a key!	Nothing useful here.	f
1	Room04	Cross roads	The door back to the East is open. There are tunnels to the North and South. The floor of the Southern tunnel is covered with human bones.	Two ways to choose!	Back in the cross roads.	f
1	Room05	Armory	This looks like a place they used to store weapons. A staircase leads down to the North.	You found a magnifient, if not magic, sword!		f
1	Room07	The Sapphire Room	All the walls are made of blue sapphire.	From a glittering platform you pick a blue key.	No more keys here!	f
1	Room06	The Beast	The home cave of the Great Beast of these dungeons. Human remains everywehere.	The stink is unbelievable.	The smell is still unbearable.	f
1	Room09	Death	You brave little fool! The monester rips you apart and your bones shall lay on the floor all eternity.			t
1	Room11	The Smaragd Chamber	This room has been dug inside enormous smaragd. Everything shines in red!	You pick up the red smaragd key!		f
1	Room12	The Treasure Hall	You found the treasure. There is gold and jewelry everywhere!	Too bad you could never carry it away...		t
1	Room10	The Gate	You hit the monster, it attacks, but you slip between it's legs through the Southern doorway.	There is huge gate, with blue and red locks.	Gate and the locks still loom ahead.	f
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, locked, adm, username, password) FROM stdin;
1	f	t	admin	pbkdf2:sha256:260000$56NcyPWPdBROTmfU$e79422d25c0762e1ec4909a467fda1840495aee7f03905ff08e0d0d41472858b
2	f	f	Rudolf	pbkdf2:sha256:260000$M8ouLxlq0ND2l9ma$2a5785caabbdab68d8fa96459d0052bb8f57139b67089fa701e26b7c5b4a64a8
\.


--
-- Data for Name: visited_rooms; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.visited_rooms (game_id, room_tag, player_id) FROM stdin;
\.


--
-- Name: conditions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.conditions_id_seq', 22, true);


--
-- Name: games_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.games_id_seq', 1, true);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.messages_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: banned_words banned_words_word_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.banned_words
    ADD CONSTRAINT banned_words_word_key UNIQUE (word);


--
-- Name: conditions conditions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conditions
    ADD CONSTRAINT conditions_pkey PRIMARY KEY (id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (tag, game_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- PostgreSQL database dump complete
--

