-- Create Teams Table
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- Create Drivers Table
CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    team_id INTEGER REFERENCES teams(id)
);

-- Create Driver Rankings Table
CREATE TABLE driver_rankings (
    id SERIAL PRIMARY KEY,
    driver_id INTEGER REFERENCES drivers(id),
    points INTEGER NOT NULL DEFAULT 0,
    position INTEGER NOT NULL,
    wins INTEGER NOT NULL DEFAULT 0
);

-- Create Constructor Standings Table
CREATE TABLE constructor_standings (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id),
    points INTEGER NOT NULL DEFAULT 0,
    position INTEGER NOT NULL
);

-- Create Questions Table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    team_id INT REFERENCES teams(id),  -- Optional reference to teams
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Responses Table
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    response_message TEXT NOT NULL,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Categories Table (Optional)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Create Question-Categories Join Table (Optional)
CREATE TABLE question_categories (
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, category_id)
);

-- Add indexes for performance (optional but recommended)
CREATE INDEX idx_drivers_team_id ON drivers(team_id);
CREATE INDEX idx_driver_rankings_driver_id ON driver_rankings(driver_id);
CREATE INDEX idx_constructor_standings_team_id ON constructor_standings(team_id);
CREATE INDEX idx_questions_team_id ON questions(team_id);  -- Index for questions
