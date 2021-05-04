--
-- PostgreSQL database dump
--
 
-- Dumped from database version 13.1 (Ubuntu 13.1-1.pgdg18.04+1)
-- Dumped by pg_dump version 13.1 (Ubuntu 13.1-1.pgdg18.04+1)
 
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
 
--
-- Name: blacklisted(integer); Type: FUNCTION; Schema: public; Owner: postgres
--
 
CREATE FUNCTION public.blacklisted(integer) RETURNS boolean
    LANGUAGE sql STRICT
    AS $_$select $1 in (select user_id from blacklist);$_$;
 
 
ALTER FUNCTION public.blacklisted(integer) OWNER TO postgres;
 
SET default_tablespace = '';
 
SET default_table_access_method = heap;
 
--
-- Name: blacklist; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.blacklist (
    user_id bigint NOT NULL,
    reason text NOT NULL
);
 
 
ALTER TABLE public.blacklist OWNER TO postgres;
 
--
-- Name: economy; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.economy (
    user_id bigint NOT NULL,
    bank integer DEFAULT 0,
    cash integer DEFAULT 0,
    debt integer DEFAULT 0,
    CONSTRAINT positive_debt CHECK ((debt >= 0))
);
 
 
ALTER TABLE public.economy OWNER TO postgres;
 
--
-- Name: guilds; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.guilds (
    guild_id bigint NOT NULL,
    bot_channel bigint
);
 
 
ALTER TABLE public.guilds OWNER TO postgres;
 
--
-- Name: inventories; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.inventories (
    user_id bigint,
    stock integer,
    chicken integer,
    heist integer
);
 
 
ALTER TABLE public.inventories OWNER TO postgres;
 
--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.messages (
    message_id bigint NOT NULL,
    author bigint NOT NULL,
    channel bigint NOT NULL,
    message_time timestamp without time zone NOT NULL,
    guild_id bigint
);
 
 
ALTER TABLE public.messages OWNER TO postgres;
 
--
-- Name: notes; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.notes (
    user_id bigint,
    raw_note text,
    note_id integer NOT NULL,
    reminder boolean DEFAULT false
);
 
 
ALTER TABLE public.notes OWNER TO postgres;
 
--
-- Name: notes_note_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--
 
CREATE SEQUENCE public.notes_note_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 
 
ALTER TABLE public.notes_note_id_seq OWNER TO postgres;
 
--
-- Name: notes_note_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--
 
ALTER SEQUENCE public.notes_note_id_seq OWNED BY public.notes.note_id;
 
 
--
-- Name: pins; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.pins (
    pin_id integer NOT NULL,
    synopsis character(33) NOT NULL,
    jump_url character(92) NOT NULL,
    author bigint NOT NULL,
    pin_date date NOT NULL,
    name character varying(20) DEFAULT ''::character varying,
    guild_id bigint
);
 
 
ALTER TABLE public.pins OWNER TO postgres;
 
--
-- Name: pins_pin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--
 
CREATE SEQUENCE public.pins_pin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 
 
ALTER TABLE public.pins_pin_id_seq OWNER TO postgres;
 
--
-- Name: pins_pin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--
 
ALTER SEQUENCE public.pins_pin_id_seq OWNED BY public.pins.pin_id;
 
 
--
-- Name: role_names; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.role_names (
    name_id integer NOT NULL,
    role_name character varying(25) NOT NULL,
    author bigint
);
 
 
ALTER TABLE public.role_names OWNER TO postgres;
 
--
-- Name: role_names_name_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--
 
ALTER TABLE public.role_names ALTER COLUMN name_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.role_names_name_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
 
 
--
-- Name: shop; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.shop (
    item_id integer NOT NULL,
    item_name character varying(25),
    stock integer,
    price integer NOT NULL,
    CONSTRAINT positive_price CHECK ((price >= 15)),
    CONSTRAINT positive_stock CHECK ((stock >= 0))
);
 
 
ALTER TABLE public.shop OWNER TO postgres;
 
--
-- Name: shop_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--
 
CREATE SEQUENCE public.shop_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 
 
ALTER TABLE public.shop_item_id_seq OWNER TO postgres;
 
--
-- Name: shop_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--
 
ALTER SEQUENCE public.shop_item_id_seq OWNED BY public.shop.item_id;
 
 
--
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.tags (
    tag_name character varying(25) NOT NULL,
    content text NOT NULL,
    author bigint,
    guild_id bigint
);
 
 
ALTER TABLE public.tags OWNER TO postgres;
 
--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.tasks (
    task_id integer,
    exec_time timestamp without time zone NOT NULL
);
 
 
ALTER TABLE public.tasks OWNER TO postgres;
 
--
-- Name: user_details; Type: TABLE; Schema: public; Owner: postgres
--
 
CREATE TABLE public.user_details (
    user_id bigint NOT NULL,
    zodiac character varying(25) DEFAULT ''::character varying,
    bday date NOT NULL,
    guild_id bigint NOT NULL
);
 
 
ALTER TABLE public.user_details OWNER TO postgres;
 
--
-- Name: notes note_id; Type: DEFAULT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.notes ALTER COLUMN note_id SET DEFAULT nextval('public.notes_note_id_seq'::regclass);
 
 
--
-- Name: pins pin_id; Type: DEFAULT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.pins ALTER COLUMN pin_id SET DEFAULT nextval('public.pins_pin_id_seq'::regclass);
 
 
--
-- Name: shop item_id; Type: DEFAULT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.shop ALTER COLUMN item_id SET DEFAULT nextval('public.shop_item_id_seq'::regclass);
 
 
--
-- Name: blacklist blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.blacklist
    ADD CONSTRAINT blacklist_pkey PRIMARY KEY (user_id);
 
 
--
-- Name: economy economy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.economy
    ADD CONSTRAINT economy_pkey PRIMARY KEY (user_id);
 
 
--
-- Name: guilds guilds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.guilds
    ADD CONSTRAINT guilds_pkey PRIMARY KEY (guild_id);
 
 
--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);
 
 
--
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (note_id);
 
 
--
-- Name: pins pins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.pins
    ADD CONSTRAINT pins_pkey PRIMARY KEY (pin_id);
 
 
--
-- Name: role_names role_names_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.role_names
    ADD CONSTRAINT role_names_role_name_key UNIQUE (role_name);
 
 
--
-- Name: shop shop_item_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.shop
    ADD CONSTRAINT shop_item_name_key UNIQUE (item_name);
 
 
--
-- Name: shop shop_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.shop
    ADD CONSTRAINT shop_pkey PRIMARY KEY (item_id);
 
 
--
-- Name: tags tags_content_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_content_key UNIQUE (content);
 
 
--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tag_name);
 
 
--
-- Name: user_details user_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.user_details
    ADD CONSTRAINT user_details_pkey PRIMARY KEY (user_id);
 
 
--
-- Name: inventories inventories_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.inventories
    ADD CONSTRAINT inventories_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.economy(user_id) ON DELETE CASCADE;
 
 
--
-- Name: messages messages_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_author_fkey FOREIGN KEY (author) REFERENCES public.economy(user_id);
 
 
--
-- Name: messages messages_guild_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds(guild_id);
 
 
--
-- Name: pins pins_guild_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.pins
    ADD CONSTRAINT pins_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds(guild_id);
 
 
--
-- Name: role_names role_names_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.role_names
    ADD CONSTRAINT role_names_author_fkey FOREIGN KEY (author) REFERENCES public.economy(user_id) ON DELETE CASCADE;
 
 
--
-- Name: tags tags_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_author_fkey FOREIGN KEY (author) REFERENCES public.economy(user_id);
 
 
--
-- Name: tags tags_guild_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds(guild_id);
 
 
--
-- Name: tasks tasks_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.notes(note_id) ON DELETE CASCADE;
 
 
--
-- Name: user_details user_details_guild_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.user_details
    ADD CONSTRAINT user_details_guild_id_fkey FOREIGN KEY (guild_id) REFERENCES public.guilds(guild_id);
 
 
--
-- Name: user_details user_details_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--
 
ALTER TABLE ONLY public.user_details
    ADD CONSTRAINT user_details_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.economy(user_id) ON DELETE CASCADE;
 
 
--
-- PostgreSQL database dump complete
--