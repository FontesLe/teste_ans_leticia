CREATE DATABASE IF NOT EXISTS ans_dados_abertos;
USE ans_dados_abertos;

CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(100),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE,
    INDEX idx_operadora_razao_social (razao_social),
    INDEX idx_operadora_uf (uf)
);

CREATE TABLE IF NOT EXISTS demonstracoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20) NOT NULL,
    data DATE NOT NULL,
    conta VARCHAR(255) NOT NULL,
    descricao_conta VARCHAR(255),
    valor DECIMAL(15,2) NOT NULL,
    periodo VARCHAR(10) NOT NULL,
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans),
    INDEX idx_dem_registro_ans (registro_ans),
    INDEX idx_dem_data (data),
    INDEX idx_dem_conta (conta(100)),
    INDEX idx_dem_periodo (periodo)
);