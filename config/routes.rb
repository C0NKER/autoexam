Examui::Application.routes.draw do
  resources :pregunta
  resources :asignaturas

  devise_for :users

  get 'nueva_pregunta/:id' => 'asignaturas#nueva_pregunta', :as => :nueva_pregunta

  root 'asignaturas#index'
end
