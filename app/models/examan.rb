class Examan < ActiveRecord::Base
  belongs_to :asignatura
  has_and_belongs_to_many :pregunta

  def listado_de_etiquetas
    self.etiquetas.to_s.split(',').map {|e| e.strip }
  end

  def clave(pregunta)
    ClavePregunta.where(:preguntum_id => pregunta.id).where(:examan_id => self.id).first_or_create
  end

  def cantidad(etiqueta)
    cantidades = preguntas_por_tema.split('|')
    for c in cantidades
      etiq, cant = c.split(':')
      if etiq == etiqueta
        return cant.to_i
      end
    end
    return 0
  end
end
