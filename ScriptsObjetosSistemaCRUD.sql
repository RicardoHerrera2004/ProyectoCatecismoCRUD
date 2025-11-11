
--Creacion de esquemas para sp, vistas y objetos programables
CREATE SCHEMA Programas
GO

--Creacion de la vista de estudiantes para el programa en py
CREATE VIEW Programas.VW_Estudiantes
AS
SELECT 
PP.PersonaId PersonaID
, PP.nombrePersona Nombre
, PP.apellidoPersona Apellido
, PP.nroDoc Identificacion
, PP.emailPersona Email
, PP.telefonoPersona Telefono
FROM Persona.Persona PP
INNER JOIN Persona.Estudiante PE
ON PE.Persona_PersonaId = PP.PersonaId

/*
	SELECT * FROM Programas.VW_Estudiantes
*/



--Creacion de sp para insertar estudiantes
ALTER PROCEDURE Programas.SP_InsertarEstudiante
    @nombrePersona      t_nombrePeque,
    @apellidoPersona    t_nombrePeque,
    @tipoDoc            t_tipo,
    @nroDoc             t_codigo,
    @fechaNacimiento    t_fecha,
    @telefonoPersona    VARCHAR(80),
    @emailPersona       t_email,
    @fechaBautismo      t_fecha = NULL,
    @lugarBautismo      t_nombreLar = NULL,
    @observacion        t_textoMed = NULL
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @PersonaId INT;
    DECLARE @t TABLE (PersonaId INT);

    BEGIN TRY
        BEGIN TRAN;

        INSERT INTO Persona.Persona
            (nombrePersona, apellidoPersona, tipoDoc, nroDoc,
             fechaNacimientoPersona, telefonoPersona, emailPersona)
        OUTPUT inserted.PersonaId INTO @t(PersonaId)
        VALUES
            (@nombrePersona, @apellidoPersona, @tipoDoc, @nroDoc,
             @fechaNacimiento, @telefonoPersona, @emailPersona);

        SELECT @PersonaId = PersonaId FROM @t;

        INSERT INTO Persona.Estudiante
            (fechaBautismo, lugarBautismo, observacion, Persona_PersonaId)
        VALUES
            (@fechaBautismo, @lugarBautismo, @observacion, @PersonaId);

        COMMIT TRAN;

        SELECT @PersonaId AS PersonaIdCreada;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRAN;
        THROW;
    END CATCH
END;
GO

/*
	EXEC Programas.SP_InsertarEstudiante
    @nombrePersona   = 'Juan',
    @apellidoPersona = 'Pérez',
    @tipoDoc         = 'CI',
    @nroDoc          = '12345678',
    @fechaNacimiento = '2005-01-15',
    @telefonoPersona = '099999999',
    @emailPersona    = 'juan.perez@test.com',
    @fechaBautismo   = '2015-05-10',
    @lugarBautismo   = 'Quito',
    @observacion     = 'Estudiante de prueba';
	GO
*/

--Creacion del sp para actualizar datos estudiantes
ALTER PROCEDURE Programas.SP_ActualizarEstudiante
    @PersonaId          t_id,
    @nombrePersona      t_nombrePeque,
    @apellidoPersona    t_nombrePeque,
    @nroDoc             t_codigo,
    @telefonoPersona    VARCHAR(80),
    @emailPersona       t_email
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRAN;

        UPDATE Persona.Persona
        SET nombrePersona          = @nombrePersona,
            apellidoPersona        = @apellidoPersona,
            nroDoc                 = @nroDoc,
            telefonoPersona        = @telefonoPersona,
            emailPersona           = @emailPersona
        WHERE PersonaId = @PersonaId;

        COMMIT TRAN;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRAN;
        THROW;
    END CATCH
END;
GO

/*
	EXEC Programas.SP_ActualizarEstudiante
    @PersonaId       = 5,
    @nombrePersona   = 'Juan Carlos',
    @apellidoPersona = 'Pérez',
    @nroDoc          = '12345678',
    @telefonoPersona = '098888888',
    @emailPersona    = 'juan.c.perez@test.com'
	GO
*/

--Creacion de sp para eliminar estudiantes
CREATE PROCEDURE Programas.SP_EliminarEstudiante
    @PersonaId t_id
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRAN;

        DELETE FROM Persona.Estudiante
        WHERE Persona_PersonaId = @PersonaId;

        DELETE FROM Persona.Persona
        WHERE PersonaId = @PersonaId;

        COMMIT TRAN;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRAN;
        THROW;
    END CATCH
END;
GO

/*
	EXEC Programas.SP_EliminarEstudiante 5
*/